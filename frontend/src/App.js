import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import styled, { createGlobalStyle, keyframes } from 'styled-components';
import { motion } from 'framer-motion';
import StatsPanel from './components/StatsPanel';
import ModelStatus from './components/ModelStatus';
import ThreatLog from './components/ThreatLog';

const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0a0e27;
    color: #ffffff;
    min-height: 100vh;
    overflow-x: hidden;
  }

  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
  }

  ::-webkit-scrollbar-thumb {
    background: rgba(0, 255, 150, 0.3);
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 255, 150, 0.6);
  }
`;

const pulse = keyframes`
  0% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
  100% { opacity: 1; transform: scale(1); }
`;

const AppContainer = styled.div`
  min-height: 100vh;
  padding: 0;
  background: #0a0e27;
`;

const Header = styled(motion.header)`
  background: rgba(15, 20, 45, 0.8);
  border-bottom: 1px solid rgba(0, 255, 150, 0.2);
  padding: 1.2rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
`;

const HeaderContent = styled.div`
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled.h1`
  font-size: 1.5rem;
  font-weight: 700;
  color: #00ff96;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-right: auto;
  letter-spacing: 0.5px;
`;

const Subtitle = styled.p`
  font-size: 0.85rem;
  color: #888;
  margin-left: 0.5rem;
  font-weight: 400;
`;

const StatusBadge = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 1.2rem;
  background: rgba(0, 255, 150, 0.1);
  border: 1px solid rgba(0, 255, 150, 0.4);
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #00ff96;
`;

const StatusDot = styled.div`
  width: 8px;
  height: 8px;
  background: #00ff96;
  border-radius: 50%;
  animation: ${pulse} 2s infinite;
`;

const MainContent = styled(motion.main)`
  max-width: 1600px;
  margin: 0 auto;
  padding: 2rem;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: auto auto auto;
  gap: 1.5rem;

  @media (max-width: 1400px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    padding: 1rem;
    gap: 1rem;
  }
`;

const ThreatLogContainer = styled.div`
  grid-column: 1 / -1;
`;

function App() {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [stats, setStats] = useState({
    total_flows: 0,
    threats_detected: 0,
    threats_blocked: 0,
    detection_rate: '0%',
    uptime: '00:00:00',
  });
  const [threats, setThreats] = useState([]);
  const [modelInfo, setModelInfo] = useState(null);
  const [threatTypeDistribution, setThreatTypeDistribution] = useState({});

  useEffect(() => {
    const socketConnection = io(process.env.REACT_APP_BACKEND_URL || 'http://localhost:5002');
    setSocket(socketConnection);

    socketConnection.on('connect', () => {
      setConnected(true);
      console.log('Connected to PRATIRAKSHA-Lite backend');
    });

    socketConnection.on('disconnect', () => {
      setConnected(false);
      console.log('Disconnected from backend');
    });

    socketConnection.on('stats_update', (data) => {
      setStats(data);
    });

    socketConnection.on('new_threat', (threat) => {
      console.log('New threat received:', threat);
      setThreats(prev => [threat, ...prev.slice(0, 49)]);
      
      // Update threat distribution
      setThreatTypeDistribution(prev => ({
        ...prev,
        [threat.threat_type]: (prev[threat.threat_type] || 0) + 1
      }));
    });

    socketConnection.on('model_info', (info) => {
      setModelInfo(info);
    });

    return () => {
      socketConnection.disconnect();
    };
  }, []);

  return (
    <>
      <GlobalStyle />
      <AppContainer>
        <Header
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          transition={{ type: "spring", stiffness: 100 }}
        >
          <HeaderContent>
            <div>
              <Logo>🛡️ PRATIRAKSHA-Lite</Logo>
              <Subtitle>AI Network Security</Subtitle>
            </div>
            <StatusBadge
              animate={{ scale: connected ? 1 : 0.95 }}
              transition={{ duration: 0.3 }}
            >
              <StatusDot />
              {connected ? 'Connection Active' : 'Disconnected'}
            </StatusBadge>
          </HeaderContent>
        </Header>

        <MainContent
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.8 }}
        >
          <StatsPanel stats={stats} threatTypeDistribution={threatTypeDistribution} />
          <ThreatLogContainer>
            <ThreatLog threats={threats} />
          </ThreatLogContainer>
        </MainContent>
      </AppContainer>
    </>
  );
}

export default App;
