import React from "react";
import { NavLink, useLocation } from "react-router-dom";
import logo from "../assets/tklbn-logo.png";

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="h-16 flex items-center justify-between bg-maroon px-6 font-montserrat">
      <div className="flex items-center">
        <img src={logo} alt="Takluban Logo" className="h-10" />
      </div>
      <span className="text-white text-lg font-bold uppercase tracking-wide text-center flex-grow">
        Filipino Native Language Profane Detection
      </span>
      <div className="flex space-x-6">
        <NavLink 
          to="/home" 
          className={({ isActive }) => 
            `text-white text-sm uppercase transition duration-300 hover:text-yellow-400 ${isActive ? 'font-bold' : ''}`
          }
          
          onClick={(ensure) => {
            if (location.pathname === '/home') {
              ensure.preventDefault(); 
            }
          }}
        >
          Home
        </NavLink>
        <NavLink 
          to="/creator" 
          className={({ isActive }) => 
            `text-white text-sm uppercase transition duration-300 hover:text-yellow-400 ${isActive ? 'font-bold' : ''}`
          }
        >
          About Us
        </NavLink>
        <NavLink 
          to="/faqs" 
          className={({ isActive }) => 
            `text-white text-sm uppercase transition duration-300 hover:text-yellow-400 ${isActive ? 'font-bold' : ''}`
          }
        >
          FAQs
        </NavLink>
      </div>
    </nav>
  );
};

export default Navbar;
