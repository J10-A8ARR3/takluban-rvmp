import React from "react";
import { Link } from "react-router-dom"; 
import logo from "../assets/tklbn-logo.png"; 

const Navbar = () => {
  return (
    <nav className="h-16 flex items-center justify-between bg-maroon px-6 font-montserrat mb-12">
      <div className="flex items-center">
        <img src={logo} alt="Takluban Logo" className="h-10" />
      </div>
      <span className="text-white text-lg font-bold uppercase tracking-wide text-center flex-grow">
        Filipino Native Language Profane Detection
      </span>
      <div className="flex space-x-6">
        <Link to="/" className="text-white text-sm uppercase transition duration-300 hover:text-yellow-400">
          Home
        </Link>
        <Link to="/creator" className="text-white text-sm uppercase transition duration-300 hover:text-yellow-400">
          About Us
        </Link>
        <Link to="/faqs" className="text-white text-sm uppercase transition duration-300 hover:text-yellow-400">
          FAQs
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
