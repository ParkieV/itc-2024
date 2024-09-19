import { Style, Stroke, Circle, Fill } from 'ol/style';

const lineStyle = new Style({
  stroke: new Stroke({
    color: '#0000CC', // Red color
    width: 4, // Line width
  }),
});

const boundaryStyle = new Style({
  image: new Circle({
    radius: 8,
    fill: new Fill({ color: 'yellow' }),
  }),
});

export { lineStyle, boundaryStyle };
