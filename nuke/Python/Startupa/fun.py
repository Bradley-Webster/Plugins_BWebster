import hiero
import bb_python.Workspace as bbw
import os
import shotgun_utils as su
import pprint

def upload_cut_data_for_sequence(sequence):
    cut_data=get_cut_data()
    cut_item_data=get_cut_item_data(sequence)
    upload_cut_and_cut_items(cut_data,cut_item_data)

def get_cut_data():
    data={"code":"test_cut_A"}

    return data


def get_cut_item_data(sequence):

    last_frame=get_last_frame(sequence)
    first_frame=get_first_frame(sequence)
    padding=first_frame
    print first_frame,"->",last_frame

    current_item=None
    current_item_edit_in=0
    cut_items=[]
    for frame in range(first_frame,last_frame):
        item_at_frame=sequence.trackItemAt(frame)

        if item_at_frame.source():
            if current_item!=item_at_frame:

                if current_item:
                    edit_range=(current_item_edit_in,frame-1)
                    cut_item = track_item_to_cut_item(current_item,edit_range)
                    cut_item = remove_start_padding_from_cut_item(cut_item,padding)
                    cut_item = add_descriptive_name_to_cut_item(cut_item)
                    if len(cut_items) and cut_items[-1]["ref_data"]["publish_path"]==cut_item["ref_data"]["publish_path"]:
                        cut_item = combine_cut_item_dicts(cut_items[-1],cut_item)
                        cut_item = add_duration_to_cut_item(cut_item)
                        cut_items[-1]=cut_item
                    else:
                        cut_item = add_index_to_cut_item(cut_item,len(cut_items))
                        cut_items.append(cut_item)
                


                current_item_edit_in = frame
                current_item = item_at_frame
    return cut_items


def track_item_to_cut_item(track_item,edit_range):
    
    item_dict={
        "sg_data":{
                "cut_item_in":get_frame_of_track_item_from_sequence_frame(track_item,edit_range[0]),
                "cut_item_out":get_frame_of_track_item_from_sequence_frame(track_item,edit_range[1]),
                "edit_in":edit_range[0],
                "edit_out":edit_range[1],
                "cut_item_duration":edit_range[1]-edit_range[0]
                },
        "ref_data":{
                "workspace":get_item_workspace_path(track_item),
                "publish_path":get_item_publish_path(track_item),
                "track_name":track_item.parent().name(),
                }
    }
    return item_dict

def remove_start_padding_from_cut_item(cut_item,padding):
    cut_item['sg_data']['edit_in']=int(cut_item['sg_data']['edit_in']-padding)
    cut_item['sg_data']['edit_out']=int(cut_item['sg_data']['edit_out']-padding)
    return cut_item

def add_duration_to_cut_item(cut_item):
    duration=cut_item['sg_data']['cut_item_out']-cut_item['sg_data']['cut_item_in']
    cut_item['sg_data']['cut_item_duration']=duration
    return cut_item

def add_index_to_cut_item(cut_item,index):
    cut_item['sg_data']['cut_order']=index
    return cut_item

def add_descriptive_name_to_cut_item(cut_item):
    cut_item['sg_data']['code']=cut_item['ref_data']['track_name']
    return cut_item

def get_frame_of_track_item_from_sequence_frame(track_item,sequence_frame):
    cut_in=int(track_item.sourceIn())+int(track_item.source().mediaSource().timecodeStart())
    edit_in=int(track_item.timelineIn())
    frames_into_item=sequence_frame-edit_in
    frame_of_item=cut_in+frames_into_item
    return frame_of_item
    

def get_last_frame(sequence):
    last=0
    for video_track in sequence.videoTracks():
        if len(video_track.items()):
            last_in_track=video_track.items()[-1].timelineOut()
            if last_in_track > last:
                last = last_in_track
    return last

def get_first_frame(sequence):
    first=None
    for video_track in sequence.videoTracks():
        if len(video_track.items()):
            first_in_track=video_track.items()[0].timelineIn()
            if not first or first_in_track < first:
                first = first_in_track

    return first


def get_item_workspace_path(item):
    file_path=item.source().mediaSource().firstpath()
    workspace=bbw.Workspace(os.path.dirname(file_path))
    return str(workspace.path)

def get_item_publish_path(item):
    file_path=item.source().mediaSource().firstpath()
    while file_path!="" and file_path!="/" :
        file_path=os.path.dirname(file_path)
        job_data_path=os.path.join(file_path,".jobdata")
        if os.path.exists(job_data_path):
            break
    return file_path


def combine_cut_item_dicts(cut_item_dict_a,cut_item_dict_b):
    cut_item_dict_a["sg_data"]["edit_out"]=cut_item_dict_b["sg_data"]["edit_out"]
    cut_item_dict_a["sg_data"]["cut_item_out"]=cut_item_dict_b["sg_data"]["cut_item_out"]
    cut_item_dict_a["sg_data"]["cut_item_duration"]=cut_item_dict_b["sg_data"]["cut_item_out"]-cut_item_dict_a["sg_data"]["cut_item_in"]
    return cut_item_dict_a


def upload_cut_and_cut_items(cut_data,cut_item_data):
    sg_cut = upload_cut_to_sg(cut_data)
    cut_items_with_links=link_cut_items_to_sg_entities(cut_item_data,sg_cut)
    upload_cut_items(cut_items_with_links)

def upload_cut_to_sg(cut_data):
    print os.environ.get("SHOW")
    cut_data["project"]=su.get_sg_project(os.environ.get("SHOW"))

    sg=su.get_sg_instance()
    finds=sg.find('Cut', [['project.Project.code', 'is', cut_data["project"]["code"]],['code', 'is', cut_data["code"]]])
    if finds and len(finds)!=0:
        return finds[0]
    else:   
        cut = sg.create('Cut', cut_data)
        return cut

def link_cut_items_to_sg_entities(cut_item_data,sg_cut):
    items_for_upload=[]
    sg_project=su.get_sg_project(os.environ.get("SHOW"))

    list_of_shots=su.get_sg_shots(os.environ.get("SHOW"),  more_fields=["sg_path"])
    dict_of_shots={}
    for shot in list_of_shots:
        dict_of_shots[shot["sg_path"]]=shot

    list_of_versions=su.get_sg_version_by_filters(os.environ.get("SHOW"),{'project.Project.code':os.environ.get("SHOW")}, more_fields=["sg_bundle_path"])
    dict_of_versions={}
    for version in list_of_versions:
        dict_of_versions[version["sg_bundle_path"]]=version

    for cut_item in cut_item_data:
        sg_data=cut_item["sg_data"]
        sg_data["project"]=sg_project

        if dict_of_shots.get(cut_item["ref_data"]["workspace"]):
            sg_data["shot"]=dict_of_shots.get(cut_item["ref_data"]["workspace"])

        if dict_of_versions.get(cut_item["ref_data"]["publish_path"]):
            sg_data["version"]=dict_of_versions.get(cut_item["ref_data"]["publish_path"])

        sg_data["cut"]=sg_cut
            
        items_for_upload.append(sg_data)
    return items_for_upload
    

def upload_cut_items(items):
    sg=su.get_sg_instance()
    for item in items:
        cut = sg.create('CutItem', item)
    pprint.pprint(items)


def upload_cut_reference(sequence):
    print "haah"
     
    

sequence = hiero.core.projects()[0].clipsBin()[1].items()[0].item()

# upload_cut_data_for_sequence(sequence)
upload_cut_reference(sequence)