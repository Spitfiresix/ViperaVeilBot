import "./App.css";
import FileUploadComponent from "./components/fileuploadform/fileupload";
import { RegistrationForm } from "./components/registrationform/RegistrationForm";

function App() {
  return (
    <div className="container">
      {/* <RegistrationForm /> */}
      <FileUploadComponent />
    </div>
  );
}

export default App;
