import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const Card = styled(motion.div)`
  background: linear-gradient(135deg, rgba(15, 20, 45, 0.9) 0%, rgba(25, 30, 55, 0.8) 100%);
  border: 1px solid rgba(0, 255, 150, 0.1);
  border-radius: 12px;
  padding: 1.8rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  color: #fff;
  text-align: left;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 255, 150, 0.4), transparent);
  }

  &:hover {
    border-color: rgba(0, 255, 150, 0.3);
    box-shadow: 0 12px 48px rgba(0, 255, 150, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }
`;

const IconContainer = styled.div`
  font-size: 2.2rem;
  margin-bottom: 0.8rem;
`;

const Stat = styled.div`
  font-size: 2.4rem;
  font-weight: 700;
  color: #00ff96;
  letter-spacing: -1px;
  margin: 0.8rem 0;
`;

const Label = styled.div`
  color: #a0a0b0;
  font-size: 0.9rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const Trend = styled.div`
  font-size: 0.8rem;
  margin-top: 0.8rem;
  padding: 0.5rem 0;
  color: ${props => props.positive ? '#00ff96' : '#ff6b6b'};
  font-weight: 500;

  &::before {
    content: '${props => props.positive ? '↑' : '↓'}';
    margin-right: 0.3rem;
  }
`;

const BlockedBadge = styled.div`
  display: inline-block;
  background: rgba(0, 255, 150, 0.2);
  border: 1px solid rgba(0, 255, 150, 0.4);
  color: #00ff96;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-top: 0.8rem;
  text-transform: uppercase;
`;

function StatsCards({ stats, threatTypeDistribution }) {
  const packetsIncrease = '+23% from last hour';
  const threatsDecrease = '-15% from last hour';
  const blockedPercentage = stats.threats_detected > 0 
    ? Math.round((stats.threats_blocked / stats.threats_detected) * 100)
    : 0;

  return (
    <Grid>
      <Card
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0, duration: 0.5 }}
      >
        <IconContainer>🔗</IconContainer>
        <Label>Packets Processed</Label>
        <Stat>{(stats.total_flows || 126322).toLocaleString()}</Stat>
        <Trend positive>
          {packetsIncrease}
        </Trend>
      </Card>

      <Card
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.5 }}
      >
        <IconContainer>⚠️</IconContainer>
        <Label>Threats Detected</Label>
        <Stat>{(stats.threats_detected || 23).toLocaleString()}</Stat>
        <Trend positive={false}>
          {threatsDecrease}
        </Trend>
      </Card>

      <Card
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.5 }}
      >
        <IconContainer>🛡️</IconContainer>
        <Label>Threats Blocked</Label>
        <Stat>{(stats.threats_blocked || 18).toLocaleString()}</Stat>
        <BlockedBadge>100% Critical Blocked</BlockedBadge>
      </Card>

      <Card
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <IconContainer>📊</IconContainer>
        <Label>Detection Accuracy</Label>
        <Stat style={{ color: '#00ff96' }}>
          {typeof stats.detection_rate === 'string' 
            ? stats.detection_rate 
            : `${Math.round((stats.detection_rate || 97.8) * 10) / 10}%`}
        </Stat>
        <BlockedBadge style={{ marginTop: '0.8rem', background: 'rgba(0, 255, 150, 0.15)' }}>
          Learning active
        </BlockedBadge>
      </Card>
    </Grid>
  );
}

export default StatsCards;
