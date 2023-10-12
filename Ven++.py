import zipfile, rainbowtext, colorama, os, json, requests, time, shutil, subprocess, ctypes, sys
from colorama import Fore
from InquirerPy import prompt
from tqdm import tqdm


if not os.name == "nt":
    os.system('clear')
    print("Linux isnt supported for now.")
    exit()

os.system('cls')

try:
    with open(os.environ.get('userprofile')+'/Ven++Data/data.json') as f:
        r = json.load(f)
except:
    print("Creating configuration files...")
    os.mkdir(os.environ.get('userprofile') + '/Ven++Data')
    os.mkdir(os.environ.get('userprofile') + '/Ven++Data/plugins')
    try:
        file = open(os.environ.get('userprofile') + '/Ven++Data/data.json', 'w')
    except: pass
    file.write('{}')
    file = open(os.environ.get('userprofile') + '/Ven++Data/data.json', 'r')
    r = json.load(file)
    r['repos'] = {}
    r['installedPlugins'] = []
    r['installed'] = False
    with open(os.environ.get('userprofile') + '/Ven++Data/data.json', 'w') as f:
        json.dump(r, f, indent=5)
    print("Created configuration files, please restart Ven++.")
    sys.exit(1)

print(rainbowtext.text("Ven++")+Fore.RESET+" | Custom Plugins Installer")
print("\nWelcome!")
print("Ven++ is a "+rainbowtext.text('OpenSource')+Fore.RESET+' tool to install "unsigned" plugins on Vencord.\nThe creator of Ven++ does not take any responsibility if something happens to your Discord account or computer (or anything).\n'+Fore.RED+"Vencord violates Discord's TOS. This installs Vencord, so it also breaks Discord's TOS."+Fore.RESET+"\n")

def download(url: str, fname: str, displayed: str, chunk_size=1024):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=displayed,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def installNodeJS():
    resp = requests.get("https://nodejs.org/dist/v18.18.1/node-v18.18.1-x64.msi", stream=True)
    total = int(resp.headers.get('content-length', 0))

    with open(os.environ.get('userprofile')+'/Ven++Data/NodeJSInstaller.msi', 'wb') as file, tqdm(
            desc="NodeJS",
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

    datapath = os.environ.get('userprofile')+"/Ven++Data"

    os.system(f"{os.environ.get('userprofile')}/Ven++Data/NodeJSInstaller.msi")

pluginsQueue = []

menu = [
    {
        "message": "Select a valid option:",
        "type": "list",
        "choices": ["Repos", "Plugins", "Install dependencies"]
    }
]

result = prompt(menu, vi_mode=True)

if result[0] == "Install dependencies":

    os.system('cls')
    print(rainbowtext.text("Ven++") + Fore.RESET + " | Custom Plugins Installer | Install dependencies")

    try:
        check = subprocess.check_output(["node", "-v"], stderr=subprocess.STDOUT, text=False)
    except subprocess.CalledProcessError:
        print(Fore.GREEN+"[!] "+Fore.RESET+"NodeJS isnt installed! NodeJS is required to build Vencord. Installing NodeJS...")
        installNodeJS()
        print(Fore.GREEN+"[!] "+Fore.RESET+"Installed NodeJS!")
    except FileNotFoundError:
        print(Fore.GREEN+"[!] "+Fore.RESET+"NodeJS isnt installed! NodeJS is required to build Vencord. Installing NodeJS...")
        installNodeJS()
        print(Fore.GREEN+"[!] "+Fore.RESET+"Installed NodeJS!")

    try:
        check = subprocess.check_output(["git"], stderr=subprocess.STDOUT, text=False)
    except subprocess.CalledProcessError:
        print(Fore.GREEN+"[!] "+Fore.RESET+"Git isnt installed! Git is required to build Vencord. Installing Git...")
        download(
            url="https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe",
            fname=os.environ.get('userprofile') + "/Ven++Data/GitSetup.exe", displayed="Git Setup")
        os.system(os.environ.get('userprofile')+"/Ven++Data/GitSetup.exe")
        print(Fore.GREEN+"[!] "+Fore.RESET+"Installed Git!")
    except FileNotFoundError:
        print(Fore.GREEN+"[!] "+Fore.RESET+"Git isnt installed! Git is required to build Vencord. Installing Git...")
        download(
            url="https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe",
            fname=os.environ.get('userprofile') + "/Ven++Data/GitSetup.exe", displayed="Git Setup")
        os.system(os.environ.get('userprofile') + "/Ven++Data/GitSetup.exe")
        print(Fore.GREEN + "[!] " + Fore.RESET + "Installed Git!")

    print("\nDone! Please make sure to restart your terminal.")


if result[0] == "Repos":
    os.system('cls')
    print(rainbowtext.text("Ven++") + Fore.RESET + " | Custom Plugins Installer | Repos management")
    print("Added Repos: "+str(len(r['repos'].keys()))+"\nInstalled plugins: "+str(len(r['installedPlugins']))+"\n")
    repoMenu = [
        {
            "message": "Select a valid option:",
            "type": "list",
            "choices": ["Add a repo", "Remove a repo"],
        }
    ]

    result = prompt(repoMenu, vi_mode=True)
    print("")
    if result[0] == "Add a repo":
        addRepoInput = [{"type": "input", "message": "Enter the repo plugins.json URL: "}]
        result = prompt(addRepoInput, vi_mode=True)
        req = requests.get(url=result[0]).json()
        repoInfo = req['repo']
        repoPlugins = req['plugins']
        r['repos'][repoInfo['name']] = { "name": repoInfo['name'], "url": result[0] }
        with open(os.environ.get('userprofile') + '/Ven++Data/data.json', 'w') as f: json.dump(r,f,indent=5)
        print("Repo name: "+repoInfo['name'])
        print("Repo description: "+repoInfo['description'])
        print("Plugins: "+str(len(repoPlugins))+"\n")
        print("Please restart Ven++.")

if result[0] == "Remove a repo":
    repoList = [
        {
            "message": "Select a repo to remove:",
            "type": "list",
            "choices": r['repos'].keys()
        }
    ]
    result = prompt(repoList, vi_mode=True)
    confirm = [{ "message": "You are about to remove "+r['repos'][result[0]]['name']+". Are you sure?", "type": "confirm", "default": False }]
    confirmResult = prompt(confirm, vi_mode=True)
    if confirmResult[0]:
        del r['repos'][result[0]]
        with open(os.environ.get('userprofile') + '/Ven++Data/data.json', 'w') as f: json.dump(r, f, indent=5)
        print("Removed "+result[0]+".\nPlease restart Ven++.")
        exit()

    print("Aborted.")

if result[0] == "Plugins":
    os.system('cls')
    print(rainbowtext.text("Ven++") + Fore.RESET + " | Custom Plugins Installer")
    print("Added Repos: "+str(len(r['repos'].keys()))+"\nInstalled plugins: "+str(len(r['installedPlugins']))+"\n")
    if int(len(r['repos'].keys())) == 0:
        print("Please add atleast 1 repo.\nPlease restart Ven++.")
        exit()

    print("Fetching plugins...")

    pluginsList = []


    for x in r['repos'].keys():
        req = requests.get(url=r['repos'][x]['url']).json()
        for xy in req['plugins']:
            for char in tqdm(pluginsList):
                time.sleep(0.25)

            pluginsList.append({"name": xy['name'], "source": x})



    print("\nUse TAB to select multiple plugins.\n")
    pluginsMenu = [
        {
            "message": "Select the plugins you want to install:",
            "type": "fuzzy",
            "choices": [xyz['name']+" | Source: "+xyz['source'] for xyz in pluginsList],
            "multiselect": True,
        }
    ]

    result = prompt(pluginsMenu, vi_mode=True)

    for yz in result[0]:
        pluginsQueue.append({"name": str(yz).split(" |", 1)[0], "source": str(yz).split(" | Source: ", 1)[1]})

    os.system('cls')
    print(rainbowtext.text("Ven++") + Fore.RESET + " | Custom Plugins Installer")
    text = ""
    for yzx in pluginsQueue:
        text += "- "+yzx['name']+" (Source: "+yzx['source']+")\n"
    print("\nYou are about to install:\n"+text)
    print("This is gonna uninject (Uninstall) your Vencord installation. It is gonna compile a new one with the selected plugins in it.\n")
    confirm = [{ "message": "Confirm?", "type": "confirm", "default": False }]
    confirmResult = prompt(confirm, vi_mode=True)

    if not confirmResult[0]:
        print("Aborted.")
        exit()

    os.system('cls')
    print(rainbowtext.text("Ven++") + Fore.RESET + " | Installing plugins...")
    print(Fore.YELLOW+"[!] "+Fore.RESET+"Downloading Vencord source code...")
    os.chdir(os.environ.get('userprofile')+'/Ven++Data')
    os.system('git clone https://github.com/Vendicated/Vencord.git')
    print(Fore.YELLOW+"[!] "+Fore.RESET+"Downloading plugins...")
    for plugin in pluginsQueue:
        req = requests.get(url=r['repos'][plugin['source']]['url']).json()
        for plg in req['plugins']:
            if plg['name'] == plugin['name']:
                download(url=plg['file'], fname=os.environ.get('userprofile')+"/Ven++Data/plugins/"+os.path.basename(plg['file']), displayed=plg['name'])

    os.rename(os.environ.get('userprofile')+'/Ven++Data/Vencord', os.environ.get('userprofile')+'/Ven++Data/vencord')
    print(Fore.YELLOW+"[!] "+Fore.RESET+"Extracting Plugins...")
    for file in os.listdir(os.environ.get('userprofile')+'/Ven++Data/plugins'):
        if file.endswith('.zip'):
            with zipfile.ZipFile(os.environ.get('userprofile') + '/Ven++Data/plugins/'+file) as zf:
                for member in tqdm(zf.infolist(), desc="Extracting "+file.replace('.zip', '')+" "):
                    try:
                        zf.extract(member, os.environ.get('userprofile') + "/Ven++Data/plugins")
                    except zipfile.error as e:
                        print(Fore.RED + "[!!] " + Fore.RESET + "Error in ZipFile: " + e + "...")
            os.remove(os.environ.get('userprofile')+"/Ven++Data/plugins/"+file)

    print(Fore.YELLOW+"[!] "+Fore.RESET+"Packing plugins in Vencord...")
    for root, dirs, files in os.walk(os.environ.get('userprofile') + '/Ven++Data/plugins'):
        for pluginFolder in dirs:
            for file in tqdm(dirs, unit='file'):
                path = os.path.join(root,pluginFolder)
                shutil.move(path, os.environ.get('userprofile') + '/Ven++Data/vencord/src/plugins/')
                time.sleep(0.2)
        for pluginFile in files:
            for file in tqdm(files, unit='file'):
                path = os.path.join(root, pluginFile)
                shutil.move(path, os.environ.get('userprofile') + '/Ven++Data/vencord/src/plugins/')
                time.sleep(0.1)


    print(Fore.YELLOW+"[!] "+Fore.RESET+"Uninjecting current Vencord..")

    if not r['installed']:
        print(Fore.YELLOW + "[!] " + Fore.RESET + "Ven++ isnt installed. Uninjecting using VencordInstallerCLI...")
        download(url="https://github.com/Vencord/Installer/releases/latest/download/VencordInstallerCli.exe", fname=os.environ.get("userprofile")+"/Ven++Data/vencordCLI.exe", displayed="VencordInstallerCLI")
        os.chdir(os.environ.get('userprofile')+'/Ven++Data')
        os.system("vencordCLI.exe -uninstall")

    r['installed'] = True
    with open(os.environ.get('userprofile') + '/Ven++Data/data.json', 'w') as f:
        json.dump(r, f, indent=5)

    print(Fore.YELLOW+"[!] "+Fore.RESET+"Installing required dependencies...")
    os.system(f'cmd /c npm i -g pnpm')
    os.chdir(os.environ.get('userprofile')+"/Ven++Data/vencord")
    os.system("cmd /c pnpm install --frozen-lockfile")
    print(Fore.YELLOW+"[!] "+Fore.RESET+"Building Vencord...")
    os.system("cmd /c pnpm build")
    print(Fore.YELLOW+"[!] "+Fore.RESET+"Injecting Vencord...")
    os.system("cmd /c pnpm inject")

