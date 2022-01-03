import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { HeatlhcareMainView } from './components/healthcare-main-view/HealthcareMainView';
import 'bootstrap/dist/css/bootstrap.min.css';
import { DocumentsView } from './components/documents-view/DocumentsView';
import { HandwritesView } from './components/handwrites-view/HandwritesView';
import { DiagnosisView } from './components/diagnosis-view/DiagnosisView';

function App() {
  return (
    <>
        <Router>
          <Routes>
            <Route exact path="/" element={<HeatlhcareMainView/>} />
            <Route exact path="/documents" element={<DocumentsView/>} />
            <Route exact path="/handwrites" element={<HandwritesView/>} />
            <Route exact path="/diagnosis" element={<DiagnosisView/>} />
          </Routes> 
        </Router>
        
      </>
  );
}

export default App;
