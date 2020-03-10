import React from 'react';
import { Table } from 'antd';

function Event() {
  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: text => <a>{text}</a>,
    },
    {
      title: 'Theme',
      dataIndex: 'theme',
      key: 'theme',
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
    },
    {
      title: 'Submission Date',
      dataIndex: 'submissionDate',
      key: 'submissionDate',
    },
    {
      title: 'Notification Date',
      dataIndex: 'notificationDate',
      key: 'notificationDate',
    },
    {
      title: 'Conference Date',
      dataIndex: 'conferenceDate',
      key: 'conferenceDate',
    },
  ];

  const data = [
    {
      key: '1',
      name: 'VISAWUS 2020: Victorian Transitions',
      theme: 'Victorian Interdisciplinary Studies',
      location: 'Reno, NV',
      submissionDate: '4/20/2020',
      notificationDate: '',
      conferenceDate: '10/15/20 - 10/17/20',
    },
    {
      key: '2',
      name: 'Food Futures: Humanities and Social Sciences Approaches',
      theme: 'Humanities for the Environment',
      location: 'National Sun Yat-sen University Kaohsiung, Taiwan',
      submissionDate: '3/15/2020',
      notificationDate: '',
      conferenceDate: '11/13/20 - 11/14/20',
    },
    {
      key: '3',
      name: 'International Symposium on SOCIAL NETWORK ANALYSIS, SOCIAL MEDIA, & MINING',
      theme: 'Social Network Analysis, Social Media, and Mining',
      location: 'Las Vegas, Nevada',
      submissionDate: '10/21/2019',
      notificationDate: '10/28/2019',
      conferenceDate: '12/5/19 - 12/7/19',
    },
  ];

  return (
      <div>
        <Table columns={columns} dataSource={data} />
      </div>
  );
}

export default Event;
