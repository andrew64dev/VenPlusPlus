# Ven++

The BEST Vencord mod so far.

# What is this?
This is a tool that lets u add custom plugins to Vencord. Removed plugins too!

# Why should i use this instead of a Vencord fork?
- On a Vencord mod, the creator needs to update it every time.
	- This is always up to date!
- No need to wait
	- You are coding your own plugin? You want to try a plugin that is not in Vencord? No need to ask a Vencord fork creator or the Vencord creator, just create your repo (or ask someone to add it to their repo).
- Get plugins back.
	- Vendicated is removing plugins from Vencord. Time to get them back!

# Tutorial (PLEASE READ!) (Only first time)
- Download the file from releases page
- Open it
- It is gonna create config files
- Open it again
- Select "Install dependencies"
- Wait for everything to install
- Open it again
- Repos > Add a repo
	- It must be a direct URL. No redirects.
- Open it again
- Plugins > Select the plugins you need and install. Discord will close, it will compile, download and do stuff, but ur done!

# How does this work?
It adds plugins to the plugins folder of Vencord, to then build it and inject it.

# How do i make my own repo?

This, is also easy!

- Create a file called `plugins.json`
- Inside of the json file, use this structure:

      {
	      "repo": {
	        "name": "My repo",
	        "description": "my vencord repo."
	      },
	      "plugins": [
	        {
	          "name": "Example 1 (for folders)",
	          "file": "direct url to zip file",
	          "description": "description for your plugin"
	        },
	        {
	          "name": "Example 2 (for .ts files)",
	          "file": "direct url to your .ts file",
	          "description": "description for your plugin"
	        }
	      ]
	  }
    
- Host it somewere. Remember, only direct URL to your `plugins.json`!
