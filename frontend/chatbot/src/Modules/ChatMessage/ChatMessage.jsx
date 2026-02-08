import React from "react";
import "./ChatMessage.css";

const ChatMessage = ({ message, sender, isError }) => {
  const isOutgoing = sender === "user";
  const className = isOutgoing ? "chat-outgoing" : "chat-incoming";

  return (
    <li className={`chat ${className}`}>
      {!isOutgoing && (
        <span className="material-symbols-outlined">smart_toy</span>
      )}
      <p className={isError ? "error" : ""}>{message}</p>
    </li>
  );
};

export default ChatMessage;
