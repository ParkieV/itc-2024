import { Feature } from 'ol';
import { Point } from 'ol/geom';
import { fromLonLat } from 'ol/proj';
import { Fill, Stroke, Style } from 'ol/style';
import CircleStyle from 'ol/style/Circle';

const usePoint = () => {
  const createPoint = (lon: number, lat: number, name: string) => {
    const point = new Point(fromLonLat([lon, lat]));

    // Create a style for the point
    const pointStyle = new Style({
      image: new CircleStyle({
        radius: 5,
        fill: new Fill({
          color: 'red',
        }),
        stroke: new Stroke({
          color: 'black',
          width: 1,
        }),
      }),
    });

    const pointFeature = new Feature({
      geometry: point,
    });

    pointFeature.setStyle(pointStyle);
    pointFeature.set('name', name);
    pointFeature.set('type', 'event');

    return pointFeature;
  };

  return { createPoint };
};

export default usePoint;
