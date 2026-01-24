Key Functionality
- [x] Add API Key Generator for extra security / public accessibibility
- [ ] Add Functionality similar to the Typical Gradio Audio Editor / Player in Ultimate TTS, (same UI elements) lets you cut/shorten larger clips when adding and saving Voice Samples. Also need ability to Edit or Change Voice Samples (not just delete and start over).
- [ ] Assess (do not build yet) ability to let this API Connect to multiple sources at once.  E.g., 2 instances of Ultimate TTS from two different locations using the same go -between.  a) would that make sense/have practicality? b) How would that work? Add another Preset Library for Sources? Maybe expand on the Gradio target functionality and have a bookmarking feature for now.  
- [ ] Assess (do not build yet) feasibility of making this even more dynamic.  E.g., what if we want to use a new source app entirely? Is this compatible with all gradio APIs? some examples to look at would be "Chattered" or "ChatterCraft-Pinokio" in the same Pinokio directory.
- [ ] Make the API work even more easily with menu systems.  E.g., In OpenWebUI it can show voices/models as a text field or a single select menu (I think) It would be nice to have that ability so you don't have to copy and paste from the "OpenWebUI Cheat Sheet" section. 

UI/UX fixes.
- [x] Reset button should aligned to the left of the sliders (or textfield/whatever ui widtget exists) Names can be variable width but reset button is consistent so should show up in a consistent location so they are less likely to show whereever the label ends.  
- [x] Float/numeric fields should auto size (min 3 digits maybe?) and show directly to the right of the UI widgets/sliders where both are present.  
- [x] Default ReadOnly fields can stack underneath Float/text UI widgets or select menus and should be appropriately sized per UI/UX common standards. 
- [x] "OpenWebUI" Cheat Sheet section should be more generically named. Since this could work for more than just OpenWebUI. 
- [x] in Cheat Sheet section right now only the POST end point is shown but potentially we could list a couple other other commonly used end point examples.  Isn't there models/voice/ stream (if thats one? -- need your expertise on this).
- [x] Add a Copy to clipboard icon button next to each of the fields in the Cheat Sheet section.

Documentation.
- [x] Build a SPEC.md appropriate for this folder and subfolders ONLY.
