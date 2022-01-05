import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { HealthcareMainView } from './components/healthcare-main-view/HealthcareMainView';
import 'bootstrap/dist/css/bootstrap.min.css';
import { DocumentsView } from './components/documents-view/DocumentsView';
import { DiagnosisView } from './components/diagnosis-view/DiagnosisView';
import { LoginView } from './components/login-view/LoginView';
import { LogoutView } from './components/logout-view/LogoutView';

function App(props) {

  return (
    <>
        <Router>
          <Routes>
            <Route exact path="/" element={<HealthcareMainView />} />
            <Route exact path="/login" element={<LoginView/>} />
            <Route exact path="/logout" element={<LogoutView/>} />
            <Route exact path="/documents" element={<DocumentsView/>} />
            <Route exact path="/diagnosis" element={<DiagnosisView/>} />
          </Routes> 
        </Router>
        
      </>
  );
}

export default App;
