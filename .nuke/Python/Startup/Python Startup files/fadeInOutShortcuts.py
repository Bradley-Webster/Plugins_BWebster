import hiero.ui

fadeInButton = hiero.ui.findMenuAction('foundry.timeline.addFadeInTransition')
fadeInButton.setShortcut("Ctrl+F")

fadeOutButton = hiero.ui.findMenuAction('foundry.timeline.addFadeOutTransition')
fadeOutButton.setShortcut("Ctrl+Shift+F")
