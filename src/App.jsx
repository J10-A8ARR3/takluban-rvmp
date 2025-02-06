import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Index from "./pages/Index";
import Home from "./pages/Home"; 
import Creators from "./pages/Creators";
import FAQs from "./pages/FAQs";


function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <div className="flex-grow">
          <Routes>
            <Route path="/" element={<Navigate to="/index" replace />} />
            <Route path="/index" element={<Index />} />
            <Route path="/home" element={<Home />} /> 
            <Route path="/creator" element={<Creators />} />
            <Route path="/faqs" element={<FAQs />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
