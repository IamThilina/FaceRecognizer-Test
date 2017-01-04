from flask import Flask, url_for,jsonify,request
import json
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

@app.route('/post/test', methods = ['POST'])
def api_post_test():
    print ("#########")
    print (request.data)
    print ("#########")
    print (request.is_json)
    print ("#########")
    print (request.json)
    print ("##################")
    data = json.loads(request.data)
    print (data["foo"])
    return jsonify(request.data)

@app.route('/test/government/data', methods = ['POST'])
def api_test_government_data():
    response = {}
    profiles = request.json
    governmentProfiles = json.loads(profiles["government"])
    response['government'] = governmentProfiles['Everything']
    return jsonify(response)

@app.route('/test/socialmedia/data', methods = ['POST'])
def api_test_socialmedia_data():
    response = {}
    profiles = request.json
    socialMediaProfiles = json.loads(profiles["socialMedia"])
    return jsonify(response)

@app.route('/facerecognizer/merge', methods = ['POST'])
def api_facerecognizer_merge():
    response = {}
    profiles = request.json
    socialMediaProfiles = json.loads(profiles["socialMedia"])
    governmentProfiles = json.loads(profiles["government"])
    #response['profiles'] = faceRecognizer.mergeGovernmentAndSocialMediaProfiles(socialMediaProfiles["mergedSocialMediaAccounts"] ,governmentProfiles["Everything"][:3])
    response['govPicture'] =  governmentProfiles["Everything"][:3]
    #response['socialPicture'] = socialMediaProfiles["mergedSocialMediaAccounts"]
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)


