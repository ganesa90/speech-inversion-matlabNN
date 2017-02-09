# speech-inversion-matlabNN
Code to estimate Vocal Tract constriction Variables (TVs) from speech using a shallow Neural Network trained in Matlab
The Network is trained to estimate 6 Tract Variables (LA, LP, TBCL, TBCD, TTCL, TTCD) from contextualized MFCCs

Usage:
python estimate_TV_xrmb.py \<path/to/audio/file> \<output/directory>

Output is saved as a .htk file in the HTK feature format. Feature dimension per frame = 6.

