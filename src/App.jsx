import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Index from "./pages/Index";

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <div className="flex-grow">
          <Routes>
            <Route path="/" element={<Navigate to="/index" replace />} />
            <Route path="/index" element={<Index />} />
            <Route path="/home" element={<h1 className="text-center mt-10">Home Page</h1>} />
            <Route path="/creator" element={<h1 className="text-center mt-10">About Us</h1>} />
            <Route path="/faqs" element={<h1 className="text-center mt-10">FAQs</h1>} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
