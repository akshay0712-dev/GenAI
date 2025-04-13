import React from "react";
import { Link } from "react-router-dom";
const Navbar = () => {
  return (
    <>
      <div className="bg-neutral-900 px-[4vw] flex items-center gap-6 py-3 z-10 sticky top-0 w-full">
        <img src="icon.svg" alt="logo" srcSet="" className="h-20 " />
        <Link to="/" className="text-white text-3xl font-semibold">
          Chat with Mentors
        </Link>
      </div>
    </>
  );
};

export default Navbar;
