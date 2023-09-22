import { useState, useEffect, useCallback, useMemo } from "react";
import DisplayImagesFromContainer from "./containerimages";
import uploadFileToBlob, {
  getBlobsInContainer,
  isStorageConfigured,
} from "../../providers/azure-blob-storage";
import { useDropzone } from "react-dropzone";

const baseStyle = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "20px",
  borderWidth: 2,
  borderRadius: 2,
  borderColor: "#eeeeee",
  borderStyle: "dashed",
  backgroundColor: "#fafafa",
  color: "#bdbdbd",
  transition: "border .3s ease-in-out",
};

const activeStyle = {
  borderColor: "#2196f3",
};

const acceptStyle = {
  borderColor: "#00e676",
};

const rejectStyle = {
  borderColor: "#ff1744",
};

const storageConfigured = isStorageConfigured();

const FileUploadComponent = (): JSX.Element => {
  // all blobs in container
  const [blobList, setBlobList] = useState<string[]>([]);

  // current file to upload into container
  const [fileSelected, setFileSelected] = useState<File | null>();
  const [fileUploaded, setFileUploaded] = useState<string>("");

  const onDrop = useCallback((acceptedFiles: any) => {
    console.log(acceptedFiles);
    //these are theiles to upload
  }, []);

  // UI/form management
  const [uploading, setUploading] = useState<boolean>(false);
  const [inputKey, setInputKey] = useState(Math.random().toString(36));
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  useEffect(() => {
    getBlobsInContainer().then((list: any) => {
      // prepare UI for results
      setBlobList(list);
    });
  }, [fileUploaded]);

  const onFileChange = (event: any) => {
    // capture file into state
    setFileSelected(event.target.files[0]);
  };

  const onFileUpload = async () => {
    if (fileSelected && fileSelected?.name) {
      // prepare UI
      setUploading(true);

      // *** UPLOAD TO AZURE STORAGE ***
      await uploadFileToBlob(fileSelected);

      // reset state/form
      setFileSelected(null);
      setFileUploaded(fileSelected.name);
      setUploading(false);
      setInputKey(Math.random().toString(36));
    }
  };

  return (
    <div>
      <h1>Upload file to Azure Blob Storage</h1>
      <div {...getRootProps({ className: "dropzone" })}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p> Drag and drop your images here.... </p>
        ) : (
          <p> Drag 'n' drop some files here</p>
        )}
      </div>
      <div>
        <button type="submit" onClick={onFileUpload}>
          Upload!
        </button>
      </div>
    </div>
  );
};

export default FileUploadComponent;
