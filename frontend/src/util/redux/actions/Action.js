const setValue = ({ prop, value }) => ({
  type: 'set_value',
  payload: { prop, value }
});

export default setValue;
