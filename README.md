<h1 align="center">AWS Security Camera IoT Device Manager</h1>
<p>
  <img src="https://img.shields.io/badge/AWS-IAM-DD344C?logo=amazoniam&logoColor=white&style=flat-square"/>
  <img src="https://img.shields.io/badge/AWS-S3-green?logo=amazons3&logoColor=white&style=flat-square"/>
  <img src="https://img.shields.io/badge/AWS-DynamoDB-blue?logo=amazondynamodb&style=flat-square"/>
  <img src="https://img.shields.io/badge/AWS-boto3-orange?logo=amazonwebservices&style=flat-square"/>
  <img src="https://img.shields.io/badge/OpenCV-4.10.0.84-5C3EE8?logo=opencv&style=flat-square"/>
  <img src="https://img.shields.io/badge/ffmpeg-h.264-007808?logo=ffmpeg&style=flat-square"/>
</p>
<p>
  The IoT_Device_Manager is responsible for managing the IoT device (such as a Raspberry Pi) used in the cloud-based security camera system.
  <br>
  <br>
  Submodule of <a href="https://github.com/Avdieienko/AWS-Security-Camera">AWS Security Camera</a>.
  Can be used independently of parent module only with deployed AWS Infrastructure(see Setup Instructions).
</p>

<h2>Tecnhologies used</h2>

- **OpenCV Python**: Record movements and faces on recording.
- **ffmpeg**: Conversion of recording codecs to suit web streaming.
- **AWS Boto3**: Connection, role assuming, uploading & retrieving data

<h2>Setup Instructions</h2>

For AWS Infrastructure setup refer to <a href="https://github.com/Avdieienko/AWS-Security-Camera">AWS Security Camera</a>.<br>

1. Generate RSA keys by running ./scripts/gen_keys.sh script, upload private key private.pem to AWS Security Camera back-end & public key use in next step.
2. Deplow AWS Infratructure( <a href="https://github.com/Avdieienko/AWS-Security-Camera">AWS Security Camera</a> ), with encoded key parameter to be public.pem key that was generated in prev step.
3. Next run ./scripts/ffmpeg_setup.sh to install ffmpeg to your device
4. Populate configs with access keys being retrieved manually from AWS User "camera". Recommend to keep session_token empty.
5. Run main.py(don't forget to activate virtual environment and install libraries from requirements.txt)

<h2>Addition information</h2>
For opencv script explanation refer to my <a href="https://github.com/Avdieienko/Security-camera">Security camera</a> repository
