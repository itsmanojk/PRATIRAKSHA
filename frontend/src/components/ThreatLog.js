import React from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

const LogContainer = styled(motion.div)`
  background: linear-gradient(135deg, rgba(15, 20, 45, 0.8) 0%, rgba(25, 30, 55, 0.7) 100%);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(0, 255, 150, 0.1);
  border-radius: 12px;
  padding: 1.8rem;
  max-height: 600px;
  overflow: hidden;
  display: flex;
  flex-direction: column;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 255, 150, 0.2), transparent);
  }
`;

const LogTitle = styled.h2`
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const TitleIcon = styled.span`
  font-size: 1.3rem;
`;

const LogContent = styled.div`
  flex: 1;
  overflow-y: auto;
  padding-right: 0.5rem;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(0, 255, 150, 0.3);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 255, 150, 0.5);
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 2rem;
  color: #888;
  font-size: 0.9rem;
`;

const ThreatItem = styled(motion.div)`
  background: linear-gradient(135deg, 
    ${props => getThreatColor(props.threatType, 'dark')} 0%, 
    ${props => getThreatColor(props.threatType, 'darker')} 100%);
  border: 1px solid ${props => getThreatColor(props.threatType, 'border')};
  border-radius: 8px;
  padding: 1.1rem;
  margin-bottom: 0.8rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: ${props => getThreatColor(props.threatType, 'color')};
  }

  &:hover {
    border-color: ${props => getThreatColor(props.threatType, 'color')};
    box-shadow: 0 8px 24px ${props => getThreatColor(props.threatType, 'shadow')};
  }
`;

const getThreatColor = (threatType, variant) => {
  const colors = {
    'Ransomware': { color: '#ff4757', dark: 'rgba(255, 71, 87, 0.15)', darker: 'rgba(255, 71, 87, 0.1)', border: 'rgba(255, 71, 87, 0.3)', shadow: 'rgba(255, 71, 87, 0.2)' },
    'Cryptolocker': { color: '#ff6b6b', dark: 'rgba(255, 107, 107, 0.15)', darker: 'rgba(255, 107, 107, 0.1)', border: 'rgba(255, 107, 107, 0.3)', shadow: 'rgba(255, 107, 107, 0.2)' },
    'Locky': { color: '#ffa502', dark: 'rgba(255, 165, 2, 0.15)', darker: 'rgba(255, 165, 2, 0.1)', border: 'rgba(255, 165, 2, 0.3)', shadow: 'rgba(255, 165, 2, 0.2)' },
    'WannaCry': { color: '#ff6348', dark: 'rgba(255, 99, 72, 0.15)', darker: 'rgba(255, 99, 72, 0.1)', border: 'rgba(255, 99, 72, 0.3)', shadow: 'rgba(255, 99, 72, 0.2)' },
    'Benign': { color: '#00ff96', dark: 'rgba(0, 255, 150, 0.15)', darker: 'rgba(0, 255, 150, 0.1)', border: 'rgba(0, 255, 150, 0.3)', shadow: 'rgba(0, 255, 150, 0.2)' },
    'DDoS': { color: '#f368e0', dark: 'rgba(243, 104, 224, 0.15)', darker: 'rgba(243, 104, 224, 0.1)', border: 'rgba(243, 104, 224, 0.3)', shadow: 'rgba(243, 104, 224, 0.2)' },
    'Malware': { color: '#ffd700', dark: 'rgba(255, 215, 0, 0.15)', darker: 'rgba(255, 215, 0, 0.1)', border: 'rgba(255, 215, 0, 0.3)', shadow: 'rgba(255, 215, 0, 0.2)' },
  };
  return colors[threatType]?.[variant] || colors['Benign'][variant];
};

const ThreatHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.8rem;
  flex-wrap: wrap;
  gap: 0.5rem;
`;

const ThreatTime = styled.span`
  font-weight: 500;
  color: #aaa;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
`;

const ThreatType = styled.span`
  font-weight: 700;
  color: ${props => getThreatColor(props.threatType, 'color')};
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const ConfidenceBadge = styled.span`
  padding: 0.3rem 0.7rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  background: ${props => props.confidence > 80 ? 'rgba(255, 71, 87, 0.2)' : 'rgba(255, 165, 2, 0.2)'};
  color: ${props => props.confidence > 80 ? '#ff4757' : '#ffa502'};
  border: 1px solid ${props => props.confidence > 80 ? 'rgba(255, 71, 87, 0.4)' : 'rgba(255, 165, 2, 0.4)'};
`;

const ThreatDetails = styled.div`
  font-size: 0.85rem;
  color: #aaa;
  display: flex;
  gap: 1.2rem;
  flex-wrap: wrap;
`;

const ThreatDetail = styled.span`
  display: flex;
  align-items: center;
  gap: 0.4rem;
  
  strong {
    color: #ddd;
  }
`;

const BlockedBadge = styled.span`
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 700;
  background: rgba(0, 255, 150, 0.2);
  color: #00ff96;
  border: 1px solid rgba(0, 255, 150, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.3px;
`;

const ThreatLog = ({ threats }) => {
  return (
    <LogContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4, duration: 0.8 }}
    >
      <LogTitle>
        <TitleIcon>🔴</TitleIcon>
        Live Threat Detection Feed
      </LogTitle>

      <LogContent>
        {threats.length === 0 ? (
          <EmptyState>
            🔍 Monitoring network traffic... Threats will appear here in real-time.
          </EmptyState>
        ) : (
          <AnimatePresence mode="popLayout">
            {threats.map((threat, index) => (
              <ThreatItem
                key={`${threat.timestamp}-${index}`}
                threatType={threat.threat_type}
                initial={{ opacity: 0, x: -30, scale: 0.95 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                exit={{ opacity: 0, x: 30, scale: 0.95 }}
                transition={{ type: "spring", stiffness: 400, damping: 40 }}
              >
                <ThreatHeader>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', flex: 1 }}>
                    <ThreatTime>{threat.timestamp}</ThreatTime>
                    <ThreatType threatType={threat.threat_type}>{threat.threat_type}</ThreatType>
                    <ConfidenceBadge confidence={Math.round(parseFloat(threat.confidence) * 100)}>
                      {Math.round(parseFloat(threat.confidence) * 100)}% Confidence
                    </ConfidenceBadge>
                  </div>
                  <BlockedBadge>✓ Blocked</BlockedBadge>
                </ThreatHeader>

                <ThreatDetails>
                  <ThreatDetail>
                    <span>From:</span>
                    <strong>{threat.source_ip}</strong>
                  </ThreatDetail>
                  <ThreatDetail>
                    <span>To:</span>
                    <strong>{threat.dest_ip}</strong>
                  </ThreatDetail>
                  <ThreatDetail>
                    <span>Type:</span>
                    <strong>{threat.threat_type} payload identified</strong>
                  </ThreatDetail>
                </ThreatDetails>
              </ThreatItem>
            ))}
          </AnimatePresence>
        )}
      </LogContent>
    </LogContainer>
  );
};

export default ThreatLog;
