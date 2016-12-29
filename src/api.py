from flask import Flask, url_for,jsonify,request
import faceRecognizer

app = Flask(__name__)

@app.route('/')
def api_root():
    return "<h1 style='color:green'>Social Media and Government Profiles Merging Server is Running</h1>"

'''
@app.route('/demo', methods = ['GET'])
def api_demo():

'''
@app.route('/match', methods = ['POST'])
def api_match():
    profiles = request.json
    response = {}
    response['mergedSocialMediaAccounts'] = faceRecognizer.mergeGovernmentAndSocialMediaProfiles(profiles.socialMedia, profiles.government)
    return jsonify(response)

@app.route('/test/government/data', methods = ['POST'])
def api_test_government_data():
    profiles = request.json
    response = {}
    response['government'] = profiles['government']['Everything'][0]
    #response['mergedSocialMediaAccounts'] = faceRecognizer.mergeGovernmentAndSocialMediaProfiles(profiles.socialMedia, profiles.government)
    return jsonify(response)

@app.route('/test/socialmedia/data', methods = ['POST'])
def api_test_socialmedia_data():
    profiles = request.json
    response = {}
    response['social'] = profiles['socialMedia']['mergedSocialMediaAccounts'][0]
    #response['mergedSocialMediaAccounts'] = faceRecognizer.mergeGovernmentAndSocialMediaProfiles(profiles.socialMedia, profiles.government)
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=4000)