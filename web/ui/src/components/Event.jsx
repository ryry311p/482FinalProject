import React, { useState } from 'react';
import { Card, Table } from 'antd';

function Event() {
  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a, b) => a.name.charCodeAt(0) - b.name.charCodeAt(0),
    },
    {
      title: 'Theme',
      dataIndex: 'theme',
      key: 'theme',
      sorter: (a, b) => a.theme.charCodeAt(0) - b.theme.charCodeAt(0),
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
      sorter: (a, b) => a.location.charCodeAt(0) - b.location.charCodeAt(0),
    },
    {
      title: 'Submission Date',
      dataIndex: 'submission_date',
      key: 'submission_date',
      sorter: (a, b) => Date.parse(a.submission_date) - Date.parse(b.submission_date),
    },
    {
      title: 'Notification Date',
      dataIndex: 'notification_date',
      key: 'notification_date',
    },
    {
      title: 'Conference Date',
      dataIndex: 'conference_date',
      key: 'conference_date',
      sorter: (a, b) => Date.parse(a.conference_date.split(' - ')[0]) - Date.parse(b.conference_date.split(' - ')[0]),
    },
  ];

  const [state, setState] = useState({
    isFetched: false,
    events: [],
  });
  if (!state.isFetched) {
    fetch('http://127.0.0.1:5000/api/get_events')
        .then((response) => {
          let num = 0;
          return response.json().then((data) => {
            const newEvents = [];
            const receivedEvents = JSON.parse(data['events']);
            receivedEvents.forEach((event) => {
              newEvents.push({
                key: num,
                ...event,
              });
              num += 1;
            });
            setState({
              isFetched: true,
              events: newEvents,
            });
          });
        });
  }

  return (
      <div>
        <Card title="All Conferences">
          <Table columns={columns} dataSource={state.events} />
        </Card>
      </div>
  );
}

export default Event;
