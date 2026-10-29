
import win32com.client
import os
from pathlib import Path

shell = win32com.client.Dispatch("Shell.Application")
shell_ns = shell.Namespace(17)
items = shell_ns.Items()

dest = Path(r".\Projects\iseeyou\iphone 7 - gita\Media_Vault\MTP_Capture")
if dest.exists():
    import shutil
    shutil.rmtree(dest)
dest.mkdir(parents=True, exist_ok=True)

for item in items:
    name = item.Name
    print(f"Device: {name}")
    if name == "Apple iPhone":
        folder = item.GetFolder()
        sub_items = folder.Items()
        for sub in sub_items:
            sub_name = sub.Name
            print(f"  Top folder: {sub_name}")
            if sub_name == "Internal Storage":
                is_folder = sub.GetFolder()
                is_items = is_folder.Items()
                for is_item in is_items:
                    is_name = is_item.Name
                    print(f"    Item: {is_name}")
                    if is_name == "DCIM" and is_item.IsFolder:
                        dcim_folder = is_item.GetFolder()
                        dcim_items = dcim_folder.Items()
                        print(f"      DCIM: {len(list(dcim_items))} items")
                        # Reset iterator
                        dcim_items = dcim_folder.Items()
                        for f in dcim_items:
                            if f.IsFolder:
                                sub_folder = f.GetFolder()
                                sub3_items = sub_folder.Items()
                                print(f"        Subfolder: {f.Name} - {len(list(sub3_items))} files")
                                sub3_items = sub_folder.Items()
                                dest_sub = dest / f.Name
                                dest_sub.mkdir(exist_ok=True)
                                for ff in sub3_items:
                                    try:
                                        src_path = ff.Path
                                        dst_path = dest_sub / ff.Name
                                        # Use Shell item's path to copy
                                        import shutil as sh
                                        if os.path.exists(src_path):
                                            sh.copy2(src_path, dst_path)
                                        else:
                                            # MTP path - try CopyHere
                                            f.CopyHere(str(dst_path), 16)
                                    except Exception as e:
                                        print(f"          Error: {e}")
                            else:
                                try:
                                    src_path = f.Path
                                    dst_path = dest / f.Name
                                    if os.path.exists(src_path):
                                        import shutil as sh
                                        sh.copy2(src_path, dst_path)
                                    else:
                                        f.CopyHere(str(dst_path), 16)
                                except Exception as e:
                                    print(f"        Error: {e}")
