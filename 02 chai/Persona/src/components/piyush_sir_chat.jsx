import React from "react";
import PiyushSirResponse from "./PiyushSirPersona.js";
import { useEffect, useState, useRef } from "react";

const Piyush_sir_chat = () => {
  const [message, setMessage] = useState("");
  const [mes, setMes] = useState([]);

  async function PiyushSirChat() {
    if (message.trim() !== "") {
      console.log("Message sent:", message);
      setMessage("");
    }
    if (!message.trim()) return;

    // 1. Add the user message to the state immediately.
    const userMessage = { user: message };
    setMes((prev) => [...prev, userMessage]);

    // 2. Make the API call to get the model's response.
    const sir_replay = await PiyushSirResponse(message);

    // 3. Update the last message with the model's response.
    setMes((prev) => {
      const updatedMessages = [...prev];
      updatedMessages[updatedMessages.length - 1] = {
        ...updatedMessages[updatedMessages.length - 1],
        model: sir_replay,
      };
      return updatedMessages;
    });

    // setMes([...mes, { user: message, model: sir_replay }]);

    setMessage("");
    console.log("mes: ", mes);
  }
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [mes]);

  return (
    <>
      <div className="mt-4 w-[90vw] md:w-[60vw] mx-auto border-1 py-3 border-neutral-800 hover:border-neutral-700 rounded-xl p-3  h-[70vh] overflow-auto ">
        {mes.map((m, index) => {
          return (
            <div className="">
              <div className="max-w-[70vw] md:max-w-[40vw] w-fit bg-neutral-900 my-3 px-5 py-3 rounded-xl mr-0 ml-auto text-white user">
                {m.user}
              </div>
              <div className="flex flex-row items-start space-x-0">
                <img
                  src="PiyushSir.jpeg"
                  alt=""
                  srcSet=""
                  className="h-8 w-8 rounded-full z-10 border border-white "
                />
                <div className="max-w-[70vw] ml-[-15px] md:max-w-[40vw] w-fit bg-neutral-900 my-3 px-5 py-3 rounded-xl text-white piyushSir">
                  {!m.model ? "Loading..." : m.model}
                </div>
              </div>
            </div>
          );
        })}
        <div ref={bottomRef} />
      </div>
      <div className="user_message flex items-center mt-4 w-[90vw] md:w-[60vw] mx-auto">
        <textarea
          className="flex-1 bg-neutral-800 text-white rounded-l-lg px-4 py-2 min-h-10 w-[70vw] md:w-[55vw] focus:outline-none "
          placeholder="Ask Piyush Sir anything..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              PiyushSirChat();
            }
          }}
        />
        <button
          className="bg-neutral-800 text-white px-4 py-2 h-16 rounded-r-lg hover:bg-neutral-700 w-[20vw] md:w-[5vw] "
          onClick={PiyushSirChat}
        >
          <img src="/send.png" alt="" srcSet="" className="h-5" />
        </button>
      </div>
    </>
  );
};

export default Piyush_sir_chat;
