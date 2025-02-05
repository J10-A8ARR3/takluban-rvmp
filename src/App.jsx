import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Router>
      <div>
        <Navbar />
        {/* Example Routes */}
        <Routes>
          <Route path="/" element={<h1 className="text-center mt-10">Home Page</h1>} />
          <Route path="/creator" element={<h1 className="text-center mt-10">About Us</h1>} />
          <Route path="/faqs" element={<h1 className="text-center mt-10">FAQs</h1>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
