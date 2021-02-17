import tkinter as tk
import os.path as osp
import re
import sys
import tempfile
import requests
import six
import tqdm
import shutil
import os.path
from os import path
import os
from tkinter import filedialog

gd_path_def = "C:\Program Files (x86)\Steam\steamapps\common\Geometry Dash"
free_ver = "https://www.mediafire.com/file/74tzmio9jl9m6i0/zBot.dll/file"
gd_path2 = ""
zbot_ver = '1.4.4'

root = tk.Tk()
root.withdraw()

CHUNK_SIZE = 512 * 1024  # 512KB

def gdloader(gd_path):
    loader = rf'{os.getcwd()}\config\GDDLLLoader.dll'
    modified = rf'{os.getcwd()}\config\libcurl.dll'
    libcurl = fr"{gd_path}\libcurl.dll"
    if path.exists(libcurl) and path.exists(loader):
        try:
            os.rename(f"{libcurl}", r'libcurl.BACKUP')
            shutil.move(modified, gd_path)
            shutil.move(loader, gd_path)
            try:
                os.mkdir(rf"{gd_path}\adaf-dll")
            except OSError:
                print("Creation of the directory %s failed" % gd_path)
            shutil.move("zBot.dll", rf"{gd_path}\adaf-dll")
            print("[zbot installer] success!")

        except Exception as err:
            print(err)
    else:
        pass


def download_cdn(url):
    r = requests.get(url, allow_redirects=True)
    open('zBot.dll', 'wb').write(r.content)

def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]

def download(url, output, quiet):
    url_origin = url
    sess = requests.session()

    while True:
        res = sess.get(url, stream=True)
        if 'Content-Disposition' in res.headers:
            # This is the file
            break

        # Need to redirect with confiramtion
        url = extractDownloadLink(res.text)

        if url is None:
            print('Permission denied: %s' % url_origin, file=sys.stderr)
            print(
                "Maybe you need to change permission over "
                "'Anyone with the link'?",
                file=sys.stderr,
            )
            return

    if output is None:
        m = re.search(
            'filename="(.*)"', res.headers['Content-Disposition']
        )
        output = m.groups()[0]
        # output = osp.basename(url)

    output_is_path = isinstance(output, six.string_types)

    if not quiet:
        print('[zbot installer] Downloading...', file=sys.stderr)
        print('[zbot installer] From:', url_origin, file=sys.stderr)
        print(
            '[zbot installer] To:',
            osp.abspath(output) if output_is_path else output,
            file=sys.stderr,
        )

    if output_is_path:
        tmp_file = tempfile.mktemp(
            suffix=tempfile.template,
            prefix=osp.basename(output),
            dir=osp.dirname(output),
        )
        f = open(tmp_file, 'wb')
    else:
        tmp_file = None
        f = output

    try:
        total = res.headers.get('Content-Length')
        if total is not None:
            total = int(total)
        if not quiet:
            pbar = tqdm.tqdm(total=total, unit='B', unit_scale=True)
        for chunk in res.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)
            if not quiet:
                pbar.update(len(chunk))
        if not quiet:
            pbar.close()
        if tmp_file:
            f.close()
            shutil.move(tmp_file, output)
    except IOError as e:
        print(e, file=sys.stderr)
        return
    finally:
        try:
            if tmp_file:
                os.remove(tmp_file)
        except OSError:
            pass
    return output


    def mhv6(gdpath):
        x = os.listdir(os.getcwd())
        os.rename(fr'{gdpath}\\absolutedlls', "absolutedlls.txt")
        absolutedls = open(fr'{gdpath}\\absolutedlls.txt', 'w')
        absolutedls.write("hackpro.dll\n")
        absolutedls.write("zBot.dll")
        absolutedls.close()
        os.rename(fr'{gdpath}\\absolutedlls.txt', f"{gdpath}\\absolutedlls")
        for i in x:
            if i.endswith(".dll"):
                os.rename(f"{i}", r'zBot.dll')
        try:
            shutil.move('zBot.dll', gdpath)

        except Exception as err:
            print(err)


if __name__ == "__main__":
    if path.exists(gd_path_def):
        print(f"gd path found on {gd_path_def}")
        gd_folder = gd_path_def

    else:
        gd_folder = ''
        while not path.exists(gd_folder):
            gd_folder = filedialog.askdirectory(title='Select your geometry dash folder')
    print(f'installation on {gd_folder}')
    if 'absolutedlls' in os.listdir(gd_folder):
        mhv6 = True
        print("absolutedlls detected!")

    print("""ZBOT INSTALLER
    press [1] to install free version
    press [2] to install pro version""")

    choice = int(input(""))
    if choice == 2:
        # lol
        from tqdm import tqdm

        url = 'https://zbot.figmentcoding.me/static/zBot.dll'
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc='Downloading zBot pro version')
        with open('zBot.dll', 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()
        if total_size != 0 and progress_bar.n != total_size:
            print('ERROR, something went wrong')
            exit()
            pass

        if mhv6:
            try:
                mhv6(gd_folder)
            except Exception as err:
                print(err)
        elif not mhv6:
            gdloader(gd_folder)

    elif choice == 2:
        download(free_ver, output=None, quiet=False)
        if mhv6:
            mhv6(gd_folder)
        elif not mhv6:
            gdloader(gd_folder)













