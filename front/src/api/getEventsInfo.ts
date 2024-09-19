import axios from 'axios';

const getEventsInfo = async () => {
  return await axios
    .get('http://90.156.229.249:8000/api/v1/events', {
      headers: {
        authorization:
          'TQ1JLdWGA1TCPm2x1mUqkOccCcwT//4a87n+Tqx4eGzSmHM5LmuxJT11mIR5IBoP5LDakUIelGHorz7L',
        accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
    .then((res) => {
      return res.data;
    })
    .catch((e) => {
      console.error('Error occured while getting geometries for roads', e);
      return null;
    });
};

export default getEventsInfo;
