"use client";

import { useEffect, useState } from 'react';
import io, { Socket } from 'socket.io-client';

interface VideoFeedProps {
  onFaceCountChange: (count: number) => void;
}

const VideoFeed: React.FC<VideoFeedProps> = ({ onFaceCountChange }) => {
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    const socketIo = io(process.env.NEXT_PUBLIC_FLASK_URL as string);

    socketIo.on('face_detected', (data) => {
        const { message } = data;
        const countMatch = message.match(/\d+/); // Extract the number from the message
        if (countMatch) {
          onFaceCountChange(parseInt(countMatch[0]));
        }
      });

    setSocket(socketIo);

    return () => {
      socketIo.disconnect();
    };
  }, [onFaceCountChange]);

  return (
    <div style={styles.videoContainer}>
      <img
        src={`${process.env.NEXT_PUBLIC_FLASK_URL}/video_feed`}
        alt="Video Feed"
        style={styles.video}
      />
    </div>
  );
};

const styles = {
  videoContainer: {
    position: 'relative',
    display: 'inline-block',
  } as React.CSSProperties,
  video: {
    width: '640px',
    height: '480px',
    border: '2px solid #000',
  } as React.CSSProperties,
};

export default VideoFeed;
