def delete_file(file_path):
    #hellonigga
    import os
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)  # Delete the file
            return f"**File deleted:** `{file_path}`"
        except Exception as e:
            return f"**Error:** Failed to delete file `{file_path}`: `{e}`"
    else:
        return f"**Error:** Invalid file path: `{file_path}`"
