import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Onboarding from './pages/Onboarding';
import Chat from './pages/Chat';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Onboarding />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
