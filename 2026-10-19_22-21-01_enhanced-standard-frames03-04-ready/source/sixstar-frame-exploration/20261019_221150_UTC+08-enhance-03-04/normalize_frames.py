from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy import ndimage as ndi
P=Path(__file__).resolve().parent;base=np.array(Image.open(P/'reference-standard-sixstar-frame.png').convert('RGBA'))
for r in json.loads((P/'material-config.json').read_text()):
 im=Image.open(P/(r['id']+'-generated-frame-original.png')).convert('RGBA').resize((1190,1786),Image.Resampling.LANCZOS);a=np.array(im);valid=a[:,:,3]>128
 indices=ndi.distance_transform_edt(~valid,return_distances=False,return_indices=True);color=a[indices[0],indices[1],:3];color[valid]=a[valid,:3]
 Image.fromarray(np.dstack([color,base[:,:,3]])).save(r['frame'])
