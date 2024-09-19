import axios from 'axios';

const createEvent = async (id: string, object: any, boundaries: any) => {
  return await axios
    .post('http://90.156.229.249:8000/api/v1/event', {
      properties: { items: object, boundaries },
      title: 'string',
      road_chunk_id: id,
      user_id: 'string',
      plan_start_date: '2024-09-19T10:29:32.952Z',
      start_date: '2024-09-19T10:29:32.952Z',
      plan_finish_date: '2024-09-19T10:29:32.952Z',
      finish_date: '2024-09-19T10:29:32.952Z',
    })
    .then((res) => {
      return res.data;
    })
    .catch((e) => {
      console.error(e);
      return null;
    });
};

export default createEvent;
