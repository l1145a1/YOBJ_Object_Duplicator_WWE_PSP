import os
import sys
import struct
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox

FILE_HEADER = 8

def generate_pof0(file_path):
    with open(file_path, 'r+b') as p:
        p.seek(0, os.SEEK_END)
        byte_count = 0
        word = b'POF0'
        p.write(word)
        p.write(b'\x00' * 4)
        start_pof0=p.tell()
        vertex_offset =[]
        UV_offset=[]
        texture_offset=[]
        texture_count=[]
        all_offset=[]

        #mulai sini
        p.seek(0)
        word = p.read(4).decode('ascii')
        if word != "YOBJ":
            print("Invalid YOBJ file, JBOY header missing")
            return

        pof0_offset = struct.unpack('<I', p.read(4))[0]
        print(f"Read Offset {p.tell()-4}, POF0 Offset: {pof0_offset}")
        temp = struct.unpack('<I', p.read(4))[0]  # zero
        temp = struct.unpack('<I', p.read(4))[0]  # pof0 offset again
        print(f"Read Offset {p.tell()-4}, POF02 Offset: {temp}")
        if temp != pof0_offset:
            print("Invalid YOBJ file, second pof0 offset different from first")
            return

        p.read(8)  # skip two zeros
        mesh_count = struct.unpack('<I', p.read(4))[0]
        print(f"Read Offset {p.tell()-4}, Mesh Count: {mesh_count}")

        p.read(8)
        cursor = p.tell()
        all_offset.append(FILE_HEADER)
        all_offset.append(p.tell())
        mesh_offset = struct.unpack('<I', p.read(4))[0]
        print(f"Read Offset {p.tell()-4}, Mesh Offset: {mesh_offset}")

        p.seek(-12,1)
        bone_count = struct.unpack('<I', p.read(4))[0]
        print(f"Read Offset {p.tell()-4}, Bone Count: {bone_count}")

        tex_count = struct.unpack('<I', p.read(4))[0]
        print(f"Read Offset {p.tell()-4}, Texture Count: {tex_count}")

        p.read(4)
        temp = cursor
        cursor = p.tell()
        all_offset.append(p.tell())

        bone_offset = struct.unpack('<I', p.read(4))[0]
        print(f"Read Offset {p.tell()-4}, Bone Offset: {bone_offset}")

        temp = cursor
        cursor = p.tell()
        all_offset.append(p.tell())

        texname_offset = struct.unpack('<I', p.read(4))[0]
        print(f"Read Offset {p.tell()-4}, Texture Name Offset: {texname_offset}")

        temp = cursor
        cursor = p.tell()
        all_offset.append(p.tell())

        obj_groupname_offset = struct.unpack('<I', p.read(4))[0]
        print(f"Read Offset {p.tell()-4}, Object Groupname Offset: {obj_groupname_offset}")

        obj_group_count = struct.unpack('<I', p.read(4))[0]
        print(f"Read Offset {p.tell()-4}, Object Group Count: {obj_group_count}")

        p.seek(mesh_offset)

        for i in range(mesh_count):
            description_offset = p.tell();
            print   (f"Object {i} Offset {p.tell()}")
            p.read(12)  # skip two zeros
            temp1 = struct.unpack('<I', p.read(4))[0]
            texture_count.append(temp1)
            print(f"Read Offset {p.tell()-4}, Texture Count: {temp1}")

            temp = cursor
            cursor = p.tell()
            all_offset.append(p.tell())

            temp1 = struct.unpack('<I', p.read(4))[0]
            vertex_offset.append(temp1)
            print(f"Read Offset {p.tell()-4}, Vertex Offset: {temp1}")

            temp = cursor
            cursor = p.tell()
            all_offset.append(p.tell())

            temp1 = struct.unpack('<I', p.read(4))[0]
            texture_offset.append(temp1)
            print(f"Read Offset {p.tell()-4}, Texture Offset: {temp1}")

            p.read(8)
            temp = cursor
            cursor = p.tell()
            all_offset.append(p.tell())

            temp1 = struct.unpack('<I', p.read(4))[0]
            UV_offset.append(temp1)
            print(f"Read Offset {p.tell()-4}, UV Offset: {temp1}")
            p.read(28)

        for i in range(mesh_count):
            print(f"Object {i} More Detail")

            p.seek(vertex_offset[i]+16)
            temp = cursor
            cursor = p.tell()
            all_offset.append(p.tell())

            temp1 = struct.unpack('<I', p.read(4))[0]
            print(f"Read Offset {p.tell()-4}, Vertex Offset 2: {temp1}")

            p.seek(UV_offset[i]+8)
            temp = cursor
            cursor = p.tell()
            all_offset.append(p.tell())

            temp1 = struct.unpack('<I', p.read(4))[0]
            print(f"Read Offset {p.tell()-4}, UV Offset 2: {temp1}")

            p.seek(texture_offset[i]+140)
            mesh_size=[]
            mesh_offset_a=[]
            for j in range(texture_count[i]):
                print(f"Texture: {j}")

                temp1 = struct.unpack('<I', p.read(4))[0]
                mesh_size.append(temp1)
                print(f"Read Offset {p.tell()-4}, Mesh Size: {temp1}")

                temp = cursor
                cursor = p.tell()
                all_offset.append(p.tell())

                temp1 = struct.unpack('<I', p.read(4))[0]
                mesh_offset_a.append(temp1)
                print(f"Read Offset {p.tell()-4}, Texture Offset A: {temp1}")

                temp = cursor
                cursor = p.tell()
                all_offset.append(p.tell())

                temp1 = struct.unpack('<I', p.read(4))[0]
                print(f"Read Offset {p.tell()-4}, Texture Offset B : {temp1}")
                p.read(132)
            print(mesh_offset_a)
            for j in range(texture_count[i]):
                p.seek(mesh_offset_a[j]+20)
                for k in range(mesh_size[j]):
                    temp = cursor
                    cursor = p.tell()
                    all_offset.append(p.tell())

                    temp1 = struct.unpack('<I', p.read(4))[0]
                    print(f"Read Offset {p.tell()-4}, Texture {j}, Mesh {k} Offset: {temp1}")
                    p.read(12)

        #untuk mengurutkan offset setiap data yang sudah dibaca
        all_offset.sort()
        print(all_offset)
        print(len(all_offset))
        p.seek(0,os.SEEK_END)
        pof0_offset = p.tell()
        #menulis POF0 menggunakan offset yang sudah diurutkan
        for i in range(len(all_offset)-1):
            cursor = all_offset[i+1]
            temp = all_offset[i]
            count = 0
            sp = cursor - temp
            if sp <= 0xFC:
                sp = (sp >> 2) | 0x40
                p.write(struct.pack('B', sp))
                count += 1
            elif sp <= 0xFFFC:
                sp = (sp >> 2) | 0x8000
                sp = struct.pack('>H', sp)
                p.write(sp)
                count += 2
            else:
                sp = (sp >> 2) | 0xC0000000
                sp = struct.pack('>I', sp)
                p.write(sp)
                count += 4
        end_pof0=p.tell()
        p.seek(pof0_offset)
        p.read(8)
        pof0_lenght=end_pof0-start_pof0
        p.seek(pof0_offset-4)
        p.write(struct.pack('<I', pof0_lenght))

def duplicate_object(file_path, object_pilihan):
    with open(file_path, 'r+b') as f:
        #variabel
        total_length = os.fstat(f.fileno()).st_size
        mesh_object_offset = []
        mesh_texture_count = []
        mesh_vertice_header_1_offset = []
        mesh_texture_offset = []
        mesh_vertice_header_2_offset = []
        mesh_vertice_count = []

        # Membaca pof0_offset
        f.seek(4)
        pof0_offset = struct.unpack('<I', f.read(4))[0]
        print(f"Offset POF0: {pof0_offset}")

        # Menghapus POF0
        f.seek(pof0_offset+8)
        length_to_truncate = total_length - f.tell()
        pof0_file = f.read(length_to_truncate)
        f.seek(-(length_to_truncate),1)
        f.truncate(f.tell())
        print(f"Menghapus POF0 {f.tell()}, sepanjang {length_to_truncate} byte.")

        #membaca mesh_count
        f.seek(24)
        mesh_count = struct.unpack('<I', f.read(4))[0]
        print(f"Read Offset {f.tell()-4}, Mesh Count: {mesh_count}")

        #membaca texture_count
        f.read(4)
        texture_count = struct.unpack('<I', f.read(4))[0]
        print(f"Read Offset {f.tell()-4}, Texture Count: {texture_count}")

        #membaca mesh_offset
        mesh_header_offset=f.tell()
        mesh_offset = struct.unpack('<I', f.read(4))[0]
        print(f"Read Offset {f.tell()-4}, Mesh Offset: {mesh_offset}")

        #menu pilih object
        f.seek(mesh_offset+8)
        print(f"Daftar Object")
        for i in range(mesh_count):
            mesh_object_offset.append(f.tell())
            f.read(4)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_texture_count.append(value)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_vertice_header_1_offset.append(value)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_texture_offset.append(value)
            f.read(8)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_vertice_header_2_offset.append(value)
            f.read(12)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_vertice_count.append(value)
            print(f"Object {i}, Offset {mesh_object_offset[i]}, Vertice Count {mesh_vertice_count[i]}")
            f.read(20)

        #copy mesh_vertice_header_1_offset ke paling bawah
        f.seek(mesh_vertice_header_1_offset[object_pilihan]+8)
        print(f"Mesh Header 1 Offset: {f.tell()}")
        value = f.read(48)
        f.seek(0, os.SEEK_END)
        new_vertex_header_1 = f.tell()
        print(f"Menulis data ke Offset {f.tell()}")
        f.write(value)

        #copy mesh_vertice_header_2_offset ke paling bawah
        f.seek(mesh_vertice_header_2_offset[object_pilihan]+8)
        print(f"Mesh Header 2 Offset: {f.tell()}")
        value = f.read(4)
        f.seek(0, os.SEEK_END)
        new_vertex_header_2 = f.tell()
        print(f"Menulis data ke Offset {f.tell()}")
        f.write(value)
        f.write(b'\x00' * 12)

        #update offset mesh vertice header
        update_header=f.tell()-8
        f.seek(-16,1)
        vertex_offset = struct.unpack('<I', f.read(4))[0]
        f.seek(-4,1)
        f.write(struct.pack('<I',update_header))
        print(f"Menulis ulang Vertex Header 2 Offset: {f.tell()-4}, Menjadi {update_header}")
        f.seek(-44,1)
        f.write(struct.pack('<I',update_header))
        print(f"Menulis ulang Vertex Header 1 Offset: {f.tell()-4}, Menjadi {update_header}")

        #copy Vertex
        f.seek(vertex_offset+8)
        print(f"Vertex Offset: {f.tell()}")
        vertex_lenght = 32+(44*mesh_vertice_count[object_pilihan])+(24*(mesh_vertice_count[object_pilihan]-1))
        value = f.read(vertex_lenght)
        f.seek(0, os.SEEK_END)
        print(f"Menulis data ke Offset {f.tell()} dengan panjang {vertex_lenght} byte")
        f.write(value)
        f.seek(0, os.SEEK_END)
        sisa = f.tell() % 16
        print(sisa)
        f.write(b'\x00' * sisa)

        #copy Texture
        f.seek(mesh_texture_offset[object_pilihan]+8)
        cursor=f.tell()
        mesh_texture_new = []
        mesh_texture_block_count =[]
        for i in range(mesh_texture_count[object_pilihan]):
            print(f"Texture {i} Offset: {f.tell()}")
            value = f.read(144)
            cursor=f.tell()
            f.seek(0, os.SEEK_END)
            mesh_texture_new.append(f.tell())
            print(f"Menulis data ke Offset {f.tell()}")
            f.write(value)
            f.seek(-12,1)
            value=struct.unpack('<I', f.read(4))[0]
            mesh_texture_block_count.append(value)
            print(f"Texture block count: {value}")
            f.seek(cursor)

        #copy Block
        for i in range(mesh_texture_count[object_pilihan]):
            f.seek(mesh_texture_new[i])
            f.read(136)
            block_start=struct.unpack('<I', f.read(4))[0]
            print(f"Texture {i} Block Start: {block_start}")
            block_end=struct.unpack('<I', f.read(4))[0]
            print(f"Texture {i} Block End: {block_end}")
            f.seek(block_start+8)
            lenght=16*mesh_texture_block_count[i]
            value = f.read(lenght)
            f.seek(0, os.SEEK_END)
            block_start_new = f.tell()
            print(f"Texture {i} New Block Start: {f.tell()}")
            f.write(value)
            block_end_new = f.tell()
            print(f"Texture {i} New Block End: {f.tell()}")
            f.seek(mesh_texture_new[i])
            f.read(136)
            f.write(struct.pack('<I',block_start_new-8))
            f.write(struct.pack('<I',block_end_new-8))

        # Pindah Lokasi Mesh Header
        f.seek(0, os.SEEK_END)
        new_header_object = f.tell()
        f.seek(mesh_offset+8)
        cursor=f.tell()
        mesh_object_offset = []
        print(f"Copy Paste Object Header ke paling bawah")
        for i in range(mesh_count):
            #copy mesh
            print(f"Object {i}, Offset {f.tell()}")
            mesh_object = f.read(64)
            cursor=f.tell()
            #paste mesh
            f.seek(0, os.SEEK_END)
            mesh_object_offset.append(f.tell())
            print(f"Write at Offset {f.tell()}")
            f.write(mesh_object)
            f.seek(cursor)

        #adding new object
        f.seek(mesh_object_offset[object_pilihan])
        value = f.read(64)
        f.seek(0, os.SEEK_END)
        offset_object_new = f.tell()
        f.write(value)

        #update header new object
        f.seek(offset_object_new)
        f.read(8)
        f.write(struct.pack('<I', new_vertex_header_1-8))
        f.write(struct.pack('<I', mesh_texture_new[0]-8))
        f.read(8)
        f.write(struct.pack('<I', new_vertex_header_2-8))

        #update header mesh
        f.seek(24)
        f.write(struct.pack('<I', mesh_count+1))
        f.seek(36)
        f.write(struct.pack('<I', new_header_object-8))
        f.seek(0, os.SEEK_END)
        new_pof0_offset = f.tell()
        f.seek(4)
        f.write(struct.pack('<I', new_pof0_offset-8))
        f.read(4)
        f.write(struct.pack('<I', new_pof0_offset-8))

def browse_file():
    file_path = filedialog.askopenfilename(title="Select YOBJ file", filetypes=[("YOBJ files", "*.yobj"), ("All files", "*.*")])
    if file_path:
        file_path_var.set(file_path)
        update_object_list(file_path)

def update_object_list(file_path):
    object_listbox.delete(0, tk.END)
    mesh_object_offset = []
    mesh_texture_count = []
    mesh_vertice_header_1_offset = []
    mesh_texture_offset = []
    mesh_vertice_header_2_offset = []
    mesh_vertice_count = []

    with open(file_path, 'r+b') as f:
        f.seek(24)
        mesh_count = struct.unpack('<I', f.read(4))[0]
        f.seek(36)
        mesh_offset = struct.unpack('<I', f.read(4))[0]
        f.seek(mesh_offset + 8)

        for i in range(mesh_count):
            mesh_object_offset.append(f.tell())
            f.read(4)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_texture_count.append(value)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_vertice_header_1_offset.append(value)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_texture_offset.append(value)
            f.read(8)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_vertice_header_2_offset.append(value)
            f.read(12)
            value = struct.unpack('<I', f.read(4))[0]
            mesh_vertice_count.append(value)

            object_info = (f"Object {i}, Offset: {mesh_object_offset[i]}, "
                           f"Vertice Count: {mesh_vertice_count[i]}, "
                           f"Texture Count: {mesh_texture_count[i]}")
            object_listbox.insert(tk.END, object_info)

            f.read(20)

def duplicate_selected_object():
    selected = object_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No object selected")
        return
    object_index = selected[0]
    file_path = file_path_var.get()
    duplicate_object(file_path, object_index)
    generate_pof0(file_path)

    # Update the object list to reflect the newly duplicated object
    update_object_list(file_path)

    messagebox.showinfo("Success", "Object duplicated and POF0 generated")


# GUI setup
root = tk.Tk()
root.title("YOBJ Object Duplicator")

file_path_var = tk.StringVar()

# File browse
tk.Label(root, text="File:").grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, textvariable=file_path_var, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Object listbox
tk.Label(root, text="Objects:").grid(row=1, column=0, padx=10, pady=10)
object_listbox = Listbox(root, selectmode=tk.SINGLE, height=10, width=80)
object_listbox.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

# Duplicate button
duplicate_button = tk.Button(root, text="Duplicate Object", command=duplicate_selected_object)
duplicate_button.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
