# Introduction

Hello :) I have no idea how to write a README or even upload things to Github, but I'll figure that part out later.

This is a little app that I started (using AI prompt coding) to make [chorusing](https://www.youtube.com/watch?v=m5JwiNSIHxY) easier. As far as I know, the best options are Audacity and Music Speed Changer, both of which have plenty of issues.

I am unable to continue with this project since it's far outside my coding abilities. I don't ven know how to start thinking about what to do next. So, I decided to just post where it is to maybe inspire someone more experienced than I am to take it a little further.

# Goals

I wanted this app to be simple and straight foward so that anyone can try chorusing and make it an easy part of their routine.

In an ideal world, it's hosted as a site that someone can go to, but still use it locally (I don't even know if that's how things work...)

There could also be a list of audio/clips that other users (studying the same language) recently used so that people who don't want to go looking for good things to chorus could still do it easily.

# Current Features

Everything that it currently has is all I could do using LLM chatbots and my basic knowledge of python.

- Uploading and storing files (example files in the uploads folder)
- Recently used files selector
- Basic audio waveform
- Play/pause button and spacebar
- Volumn control
- Zoom control (for the waveform). Ctrl + +- also works
- Section selection and saving (saving is a little busted, but a json file is put into loops with info about the loop)
- Selection or saved loop looping (it replays after an adjustable delay)
- Enabling and disabling looping
- Direct monitoring (replaying what the mic here). The audio is currently delayed a very small amount, making it annoying to use

As it is, it actually is functional. I've used it for chorusing for about an hour total. But decided Audacity is still currently easier to work with.

# Planned Features

- [ ] Better waveform viewer. Right now, I hate that the audio moves, leaving the playhead in the middle. I think it should behave like Audacity (playhead moves leaving waveform steady).
- [ ] Audio speed controller (change the tempo of the track/a single loop with a simple interface)
- [ ] Make the "saved clips" actually be clips and have more features
 - [ ] Looping isn't working
 - [ ] No volume control or speed controls
- [ ] Make the direct monitor a low latency as humanly (and computerly) possible
- [ ] Add a "marker" feature. Markers can be placed in audio with tags as reminders and can be navigated between (and saved in the json file)
- [ ] Transcription box. On saved clips, there's a transciption box which can be filled in as listening practice. And it can be hidden/showed with a toggle. This is also saved in the json
- [ ] Online support (so that users don't need to download and run anything).
- [ ] Language selection (so that you know what languages an audio file is for)
- [ ] Audio browsing and downloading (so other users learning the same language can easily download good files for chorusing)
- [ ] If things are online, moderation would also need to be a thing...
- [ ] Better styling and design lmao

Those are pretty much all the features **I** think would make a chorusing app as complete as needed.
