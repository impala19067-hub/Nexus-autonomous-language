"""
Pure Python .deb (debian archive) builder module.
Creates valid .deb packages without requiring dpkg-deb or Linux.
"""
import os, tarfile, gzip, io, struct

def create_tar_gz(base_dir, sub_paths):
    """Create tar.gz bytes for specified paths inside base_dir."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for rel_path in sub_paths:
            full_path = os.path.join(base_dir, rel_path)
            if os.path.exists(full_path):
                # Normalize arcname
                arcname = "./" + rel_path.replace("\\", "/")
                tarinfo = tar.gettarinfo(full_path, arcname=arcname)
                if os.path.isfile(full_path):
                    with open(full_path, "rb") as f:
                        tar.addfile(tarinfo, f)
                else:
                    tar.addfile(tarinfo)
    return buf.getvalue()

def build_deb(deb_root_dir, output_deb_path):
    """Assemble a standard .deb package (ar format)."""
    # 1. debian-binary
    debian_binary = b"2.0\n"

    # 2. control.tar.gz
    ctrl_buf = io.BytesIO()
    with tarfile.open(fileobj=ctrl_buf, mode="w:gz") as tar:
        ctrl_file = os.path.join(deb_root_dir, "DEBIAN", "control")
        if os.path.exists(ctrl_file):
            tarinfo = tar.gettarinfo(ctrl_file, arcname="./control")
            tarinfo.mode = 0o644
            with open(ctrl_file, "rb") as f:
                tar.addfile(tarinfo, f)
    control_gz = ctrl_buf.getvalue()

    # 3. data.tar.gz
    data_buf = io.BytesIO()
    with tarfile.open(fileobj=data_buf, mode="w:gz") as tar:
        usr_dir = os.path.join(deb_root_dir, "usr")
        for root, dirs, files in os.walk(usr_dir):
            for d in dirs:
                full_p = os.path.join(root, d)
                rel_p = os.path.relpath(full_p, deb_root_dir).replace("\\", "/")
                tarinfo = tar.gettarinfo(full_p, arcname="./" + rel_p)
                tar.addfile(tarinfo)
            for file_name in files:
                full_p = os.path.join(root, file_name)
                rel_p = os.path.relpath(full_p, deb_root_dir).replace("\\", "/")
                tarinfo = tar.gettarinfo(full_p, arcname="./" + rel_p)
                if file_name == "nexus":
                    tarinfo.mode = 0o755
                else:
                    tarinfo.mode = 0o644
                with open(full_p, "rb") as f:
                    tar.addfile(tarinfo, f)
    data_gz = data_buf.getvalue()

    # Pack into BSD ar format
    # Global header: !<arch>\n
    # Member header format (60 bytes):
    # Name (16), Mtime (12), Owner (6), Group (6), Mode (8), Size (10), Magic (2: `\n)

    def make_ar_header(name, size):
        hdr = f"{name:<16}{'0':<12}{'0':<6}{'0':<6}{'100644':<8}{size:<10}`\n"
        return hdr.encode('ascii')

    with open(output_deb_path, "wb") as deb:
        deb.write(b"!<arch>\n")

        # Member 1: debian-binary
        deb.write(make_ar_header("debian-binary", len(debian_binary)))
        deb.write(debian_binary)

        # Member 2: control.tar.gz
        deb.write(make_ar_header("control.tar.gz", len(control_gz)))
        deb.write(control_gz)
        if len(control_gz) % 2 != 0:
            deb.write(b"\n")

        # Member 3: data.tar.gz
        deb.write(make_ar_header("data.tar.gz", len(data_gz)))
        deb.write(data_gz)
        if len(data_gz) % 2 != 0:
            deb.write(b"\n")

    print("[SUCCESS] Package built:", output_deb_path)
