import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const PanelContainer = styled(motion.div)`
  grid-column: span 2;
  background: linear-gradient(135deg, rgba(15, 20, 45, 0.8) 0%, rgba(25, 30, 55, 0.7) 100%);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(0, 255, 150, 0.1);
  border-radius: 12px;
  padding: 1.8rem;
  height: fit-content;
  transition: all 0.3s ease;

  &:hover {
    border-color: rgba(0, 255, 150, 0.2);
  }

  @media (max-width: 1200px) {
    grid-column: 1 / -1;
  }
`;

const PanelTitle = styled.h2`
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1.3rem;
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

const ChartContainer = styled.div`
  width: 100%;
  height: 300px;
  margin-top: 1rem;
`;

const LegendContainer = styled.div`
  margin-top: 1.5rem;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.8rem;
  font-size: 0.8rem;
`;

const LegendItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #aaa;
`;

const LegendColor = styled.div`
  width: 12px;
  height: 12px;
  border-radius: 2px;
  background-color: ${props => props.color};
`;

const StatsPanel = ({ stats, threatTypeDistribution }) => {
  const [chartData, setChartData] = useState([]);
  const [threatData, setThreatData] = useState([
    { name: 'Ransomware', value: 0, color: '#ff4757' },
    { name: 'Cryptolocker', value: 0, color: '#ff6b6b' },
    { name: 'Locky', value: 0, color: '#ffa502' },
    { name: 'WannaCry', value: 0, color: '#ff6348' },
    { name: 'Benign', value: 0, color: '#00ff96' }
  ]);
  
  const chartDataRef = useRef([]);
  const threatDistributionRef = useRef({});

  // Initialize chart data
  useEffect(() => {
    const initialData = Array.from({ length: 15 }, (_, i) => {
      const time = new Date(Date.now() - (14 - i) * 15000);
      return {
        time: time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        packets: 1800 + Math.random() * 1200,
        threats: Math.random() * 2
      };
    });
    chartDataRef.current = initialData;
    setChartData(initialData);
  }, []);

  // Update chart data every 5 seconds with new data point
  useEffect(() => {
    const interval = setInterval(() => {
      const newPoint = {
        time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        packets: 1800 + Math.random() * 1200,
        threats: Math.random() * 2
      };
      
      chartDataRef.current = [...chartDataRef.current.slice(-14), newPoint];
      setChartData([...chartDataRef.current]);
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);

  // Update threat distribution
  useEffect(() => {
    const threatColors = {
      'Benign': '#00ff96',
      'Cryptolocker': '#ff6b6b',
      'Locky': '#ffa502',
      'Ransomware': '#ff4757',
      'WannaCry': '#ff6348'
    };

    if (Object.keys(threatTypeDistribution).length > 0) {
      threatDistributionRef.current = { ...threatTypeDistribution };
    }

    // Build threat data with current counts
    const newThreatData = [
      { name: 'Ransomware', value: threatDistributionRef.current['Ransomware'] || 0, color: '#ff4757' },
      { name: 'Cryptolocker', value: threatDistributionRef.current['Cryptolocker'] || 0, color: '#ff6b6b' },
      { name: 'Locky', value: threatDistributionRef.current['Locky'] || 0, color: '#ffa502' },
      { name: 'WannaCry', value: threatDistributionRef.current['WannaCry'] || 0, color: '#ff6348' },
      { name: 'Benign', value: threatDistributionRef.current['Benign'] || 0, color: '#00ff96' }
    ].filter(item => item.value > 0);

    // If no threats yet, show default distribution
    if (newThreatData.length === 0) {
      setThreatData([
        { name: 'Ransomware', value: 8, color: '#ff4757' },
        { name: 'Cryptolocker', value: 6, color: '#ff6b6b' },
        { name: 'Locky', value: 5, color: '#ffa502' },
        { name: 'WannaCry', value: 4, color: '#ff6348' },
        { name: 'Benign', value: 1, color: '#00ff96' }
      ]);
    } else {
      setThreatData(newThreatData);
    }
  }, [threatTypeDistribution]);

  return (
    <>
      <PanelContainer initial="hidden" animate="show" transition={{ type: "spring", stiffness: 100 }}>
        <PanelTitle>
          <TitleIcon>📊</TitleIcon>
          Network Activity
        </PanelTitle>
        <div style={{ fontSize: '0.85rem', color: '#888' }}>Packets per 5-minute interval</div>
        <ChartContainer>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              <defs>
                <linearGradient id="colorPackets" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#00ff96" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#00ff96" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis 
                dataKey="time" 
                stroke="#666" 
                style={{ fontSize: '12px' }} 
                tick={{ fill: '#888', fontSize: 12 }}
              />
              <YAxis 
                stroke="#666" 
                style={{ fontSize: '12px' }} 
                tick={{ fill: '#888', fontSize: 12 }}
              />
              <Tooltip 
                contentStyle={{ 
                  background: 'rgba(15, 20, 45, 0.95)', 
                  border: '1px solid rgba(0, 255, 150, 0.3)', 
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="packets" 
                stroke="#00ff96" 
                strokeWidth={2.5}
                dot={false}
                animationDuration={300}
              />
              <Line 
                type="monotone" 
                dataKey="threats" 
                stroke="#ff6b6b" 
                strokeWidth={2.5}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </PanelContainer>

      <PanelContainer initial="hidden" animate="show" transition={{ type: "spring", stiffness: 100 }}>
        <PanelTitle>
          <TitleIcon>🎯</TitleIcon>
          Threat Distribution
        </PanelTitle>
        <div style={{ fontSize: '0.85rem', color: '#888' }}>Current threat landscape</div>
        <ChartContainer>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={threatData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={2}
                dataKey="value"
                animationDuration={300}
              >
                {threatData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  background: 'rgba(15, 20, 45, 0.95)', 
                  border: '1px solid rgba(0, 255, 150, 0.3)', 
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </ChartContainer>
        <LegendContainer>
          {threatData.map((threat, idx) => (
            <LegendItem key={idx}>
              <LegendColor color={threat.color} />
              <span>{threat.name} ({threat.value})</span>
            </LegendItem>
          ))}
        </LegendContainer>
      </PanelContainer>
    </>
  );
};

export default StatsPanel;
