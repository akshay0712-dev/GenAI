import React from "react";
import { Link } from "react-router-dom";

const Main = () => {
  return (
    <>
      <div className="bg-[#ccc] min-h-screen flex flex-col md:flex-row items-center justify-center gap-10 py-3">
        <Link to="hitesh_sir" className="bg-neutral-900 w-[80vw] md:w-[30vw] rounded-xl flex flex-col items-center justify-center py-3 cursor-pointer transform transition-transform duration-500 hover:scale-110">
          <div className="flex flex-row items-center justify-left w-full px-8  gap-6">
            <img
              src="HiteshSir.jpg"
              alt=""
              srcset=""
              className=" w-28 rounded-full border-2 border-white"
            />

            <div className="text-white text-xl font-bold">Hitesh Sir</div>
          </div>
          <div className="text-white w-[80%] mt-5 text-md font-medium">
            Chai ke saath hum ready hain, bhai! Puchho jo puchna hai, Code
            karenge aur chill karenge! 😄☕
          </div>
        </Link>
        <Link to="piyush_sir" className="bg-neutral-900 w-[80vw] md:w-[30vw] rounded-xl flex flex-col items-center justify-center py-3 cursor-pointer transform transition-transform duration-500 hover:scale-110 ">
          <div className="flex flex-row items-center justify-left w-full px-8  gap-6">
            <img
              src="PiyushSir.jpeg"
              alt=""
              srcset=""
              className=" w-28 rounded-full border-2 border-white"
            />

            <div className="text-white text-xl font-bold">Piyush Sir</div>
          </div>
          <div className="text-white w-[80%] mt-5 text-md font-medium">
            Dekho bhai! Full energy mein puchho jo puchna hai! 🔥😎 Hum hain
            taiyar, tumhara mentor, tumhara dost! 💻❤️
          </div>
        </Link>
      </div>
    </>
  );
};

export default Main;
