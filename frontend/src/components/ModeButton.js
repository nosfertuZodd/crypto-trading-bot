import React from 'react';
import { FaMoon, FaSun } from 'react-icons/fa';  // Import icons from react-icons/fa

const ModeButton = ({ isDarkMode, toggleMode }) => {
  return (
    <div>
      <button onClick={toggleMode} className="mode-toggle-btn">
        {/* Display different icons based on the current mode */}
        {isDarkMode ? (
          <FaSun size={20} color="yellow" /> // Sun icon for light mode
        ) : (
          <FaMoon size={20} color="black" /> // Moon icon for dark mode
        )}
      </button>
    </div>
  );
};

export default ModeButton;
