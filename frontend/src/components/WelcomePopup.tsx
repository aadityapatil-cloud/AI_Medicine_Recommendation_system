import { useEffect, useState } from "react";

interface WelcomePopupProps {
  userName?: string;
  onClose: () => void;
}

export function WelcomePopup({ userName, onClose }: WelcomePopupProps) {
  const [isClosing, setIsClosing] = useState(false);
  const [secondsRemaining, setSecondsRemaining] = useState(5);

  useEffect(() => {
    // 1-second interval to update remaining seconds display
    const interval = setInterval(() => {
      setSecondsRemaining((prev) => (prev > 1 ? prev - 1 : 0));
    }, 1000);

    // Auto-dismiss automatically after at least 5 seconds
    const autoDismissTimer = setTimeout(() => {
      handleDismiss();
    }, 5000);

    return () => {
      clearInterval(interval);
      clearTimeout(autoDismissTimer);
    };
  }, []);

  const handleDismiss = () => {
    if (isClosing) return;
    setIsClosing(true);
    setTimeout(() => {
      onClose();
    }, 300);
  };

  return (
    <div
      className={`welcome-popup-overlay ${
        isClosing ? "welcome-popup-overlay--closing" : ""
      }`}
      role="dialog"
      aria-modal="true"
      aria-labelledby="welcome-popup-heading"
    >
      <div
        className={`welcome-popup-card ${
          isClosing ? "welcome-popup-card--closing" : ""
        }`}
      >
        {/* Close (×) button available */}
        <button
          type="button"
          className="welcome-popup-close-btn"
          onClick={handleDismiss}
          aria-label="Close"
          title="Close (×)"
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        {/* Animated Medical Brand Emblem */}
        <div className="welcome-popup-emblem">
          <div className="welcome-popup-pulse-ring" />
          <div className="welcome-popup-icon-box">
            <span className="welcome-emblem-cross-v" />
            <span className="welcome-emblem-cross-h" />
            <span className="welcome-emblem-dot dot-1" />
            <span className="welcome-emblem-dot dot-2" />
            <span className="welcome-emblem-dot dot-3" />
          </div>
        </div>

        {/* Status Pill */}
        <div className="welcome-popup-pill">
          <span className="welcome-popup-dot-live" />
          <span>Session Authenticated</span>
        </div>

        {/* Required Headings: “Welcome” and “AI Medicine Recommendation System” */}
        <h1 id="welcome-popup-heading" className="welcome-popup-title">
          Welcome
        </h1>

        {userName && (
          <p className="welcome-popup-user">
            {userName}
          </p>
        )}

        <h2 className="welcome-popup-system">
          AI Medicine Recommendation System
        </h2>

        <p className="welcome-popup-desc">
          Your clinical analytics dashboard is ready with 132 machine learning
          symptom inference features and safety verification.
        </p>

        {/* 5-Second Animated Progress Bar */}
        <div className="welcome-popup-progress-container">
          <div className="welcome-popup-progress-track">
            <div className="welcome-popup-progress-fill" />
          </div>
          <div className="welcome-popup-timer-text">
            <span>
              {secondsRemaining > 0
                ? `Dismissing in ${secondsRemaining}s…`
                : "Entering dashboard…"}
            </span>
            <button
              type="button"
              className="welcome-popup-manual-dismiss"
              onClick={handleDismiss}
            >
              Enter Now &rarr;
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
