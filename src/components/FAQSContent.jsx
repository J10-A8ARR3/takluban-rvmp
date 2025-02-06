import React, { useState } from 'react';

const FAQSContent = () => {
  const [isOpen, setIsOpen] = useState(null);

  const faqData = [
    {
      question: "How does the project work?",
      answer: `The project identifies the language of a given sentence, performs POS tagging, and detects profanity.
        It uses a trained language identification model, a POS tagger, and an SVM-based profanity detection system.
        If a sentence is profane, it is censored, and results are displayed.`
    },
    {
      question: "What algorithms were used?",
      answer: (
        <ul className="list-disc ml-6">
          <li><b>Naive Bayes</b> for Language Identification</li>
          <li><b>Stanford POS Tagger</b> for POS Tagging</li>
          <li><b>Support Vector Machine & N-gram</b> for Profanity Detection</li>
        </ul>
      )
    },
    {
      question: "How to contact the creators?",
      answer: (
        <p>
          Send an email to <a href="mailto:takluban24@gmail.com" className="text-maroon-700 underline">takluban24@gmail.com</a>.<br />
          Or contact:
          <ul className="list-disc ml-6 mt-2">
            <li><b>Annalyn P. Belen</b> - <a href="mailto:annalynpelaez26@gmail.com" className="text-maroon-700 underline">annalynpelaez26@gmail.com</a></li>
            <li><b>Jeo C. Abarre</b> - <a href="mailto:jeoabarre.07@gmail.com" className="text-maroon-700 underline">jeoabarre.07@gmail.com</a></li>
            <li><b>Randolph V. Larano</b> - <a href="mailto:randolphlarano@gmail.com" className="text-maroon-700 underline">randolphlarano@gmail.com</a></li>
            <li><b>Telisha Jelena B. Gonzales</b> - <a href="mailto:tishagonzales1709@gmail.com" className="text-maroon-700 underline">tishagonzales1709@gmail.com</a></li>
          </ul>
        </p>
      )
    },
    {
      question: "Where to access the repository?",
      answer: <p>Visit <a href="https://github.com/lalanglarano/TAKLUBAN-FILIPINO-NATIVE-LANGUAGE-PROFANE-DETECTION" className="text-maroon-700 underline">GitHub Repository</a>.</p>
    }
  ];

  return (
    <div>
      <div className="max-w-2xl mx-auto mt-10">
        <h2 className="text-2xl font-bold text-center text-maroon-800 uppercase tracking-wider">
          FREQUENTLY ASKED QUESTIONS
        </h2>
        <ul className="mt-6 space-y-4">
          {faqData.map((faq, index) => (
            <li key={index} className="bg-white border border-gray-300 rounded-lg overflow-hidden">
              <button
                onClick={() => setIsOpen(isOpen === index ? null : index)}
                className={`w-full p-4 text-left cursor-pointer text-maroon-700 font-semibold bg-maroon-100 
                  ${isOpen === index ? '' : 'uppercase'}`}
              >
                {faq.question}
              </button>
              <div
                className={`transition-all duration-300 ease-in-out ${isOpen === index ? 'max-h-96 py-4' : 'max-h-0 py-0'} overflow-hidden p-4 text-gray-700`}
              >
                {typeof faq.answer === 'string' ? (
                  <p>{faq.answer}</p>
                ) : (
                  faq.answer
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default FAQSContent;
