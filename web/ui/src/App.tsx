import React from 'react';
import { Layout } from "antd";
import './App.css';
import 'antd/dist/antd.css';

import Event from "./components/Event";
const { Header, Content, Footer } = Layout;

function App() {
  return (
      <Layout className="layout">
        <Header style={{ position: "fixed", zIndex: 1, width: "100%" }}>
          <div className="logo">Event Extractor</div>
        </Header>
    <Content style={{ padding: '0 50px', marginTop: 114 }}>
      <div className="site-layout-content">
        <Event/>
      </div>
    </Content>
    <Footer style={{ textAlign: 'center' }}>CSC 482 Speech and Language Processing</Footer>
  </Layout>
  );
}

export default App;
