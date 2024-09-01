"use client";

import Head from 'next/head';
import { useState } from 'react';
import VideoFeed from '../components/VideoFeed';

const Home: React.FC = () => {
  const [faceCount, setFaceCount] = useState(0);

  const handleFaceCountChange = (count: number) => {
    setFaceCount(count);
  };

  return (
    <div style={styles.container}>
      <Head>
        <title>Face Detection</title>
      </Head>
      <h1>Face Detection Using Flask, OpenCV, and Next.js</h1>
      <VideoFeed onFaceCountChange={handleFaceCountChange} /><br/>
      <h1 className={`text-2xl ${
          faceCount === 1 ? 'text-green-500' : 'text-red-500'
        }`}>{faceCount} Faces Detected !</h1>
        {faceCount == 1 && <button className='text-cyan-300 h-5 w-25'>You are eligible to vote</button>}
    </div>
  );
};

const styles = {
  container: {
    textAlign: 'center',
    padding: '20px',
  } as React.CSSProperties,
};

export default Home;
