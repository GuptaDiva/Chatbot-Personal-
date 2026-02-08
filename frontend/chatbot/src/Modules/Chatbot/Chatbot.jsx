import React, { useState, useRef, useEffect } from "react";
import ChatMessage from "../ChatMessage/ChatMessage";
import ChatInput from "../ChatInput/ChatInput";
import "./Chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [isVisible, setIsVisible] = useState(true);
  const [showFarewellMessage, setShowFarewellMessage] = useState(false);
  const chatboxRef = useRef(null);

  useEffect(() => {
    if (chatboxRef.current) {
      chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async (userInput) => {
    if (!userInput.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: userInput,
      sender: "user",
    };
    setMessages((prev) => [...prev, userMessage]);

    const thinkingMessage = {
      id: Date.now() + 1,
      text: "Thinking...",
      sender: "bot",
      isThinking: true,
    };
    setMessages((prev) => [...prev, thinkingMessage]);

    try {
      const response = await fetch("/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "user_input=" + encodeURIComponent(userInput),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      setMessages((prev) =>
        prev.map((msg) =>
          msg.isThinking
            ? { ...msg, text: data.response, isThinking: false }
            : msg,
        ),
      );
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.isThinking
            ? {
                ...msg,
                text: "Oops! Something went wrong. Please try again!",
                isThinking: false,
                isError: true,
              }
            : msg,
        ),
      );
    }
  };

  if (!isVisible) {
    return showFarewellMessage ? (
      <p className="lastMessage">Thanks for using our Chatbot!</p>
    ) : null;
  }

  return (
    <div className="chatBot">
      <div className="chatbot-header">
        <h3>ChatBot</h3>
      </div>

      <ul className="chatbox" ref={chatboxRef}>
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message.text}
            sender={message.sender}
            isError={message.isError}
          />
        ))}
      </ul>

      <ChatInput onSendMessage={sendMessage} />
    </div>
  );
};

export default Chatbot;
