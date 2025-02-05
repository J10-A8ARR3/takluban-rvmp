import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import loadingVideo from "../assets/tklbn-loading.mp4";

const Index = () => {
  const navigate = useNavigate();
  const [showLoader, setShowLoader] = useState(false);

  const handleContinue = () => {
    setShowLoader(true);
    setTimeout(() => {
      navigate("/");
    }, 3000); // Adjust timing based on video length
  };

  useEffect(() => {
    if (showLoader) {
      const video = document.getElementById("loadingVideo");
      if (video) {
        video.play();
      }
    }
  }, [showLoader]);

  return (
    <div className="font-montserrat">
      {showLoader ? (
        <div id="loader" className="fixed inset-0 flex items-center justify-center bg-black">
          <video autoPlay muted loop id="loadingVideo" className="w-full h-full object-cover">
            <source src={loadingVideo} type="video/mp4" />
          </video>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center min-h-screen p-8 text-center">
          <img src="/static/assets/tklbn-logo-xl.png" alt="Takluban Logo" className="h-24 mb-4" />
          <h1 className="text-2xl font-bold text-gray-800 leading-tight">
            INTEGRATING POS TAGGING AND RULE GENERATION
            <br /> IN MULTILINGUAL FILIPINO NATIVE LANGUAGE
            <br /> PROFANE DETECTION
          </h1>
          <div className="mt-6">
            <button 
              className="px-6 py-2 text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700"
              onClick={handleContinue}
            >
              CONTINUE
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Index;
