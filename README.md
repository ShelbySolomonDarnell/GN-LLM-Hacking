# GN-LLM-Hacking
Code for hacking on large learning models with a GeneNetwork context.


## Use VLLM

# Call the server using curl:
curl -X POST "http://localhost:8000/v1/completions" \
	-H "Content-Type: application/json" \
    --trust_remote_code \
	--data '{
		"model": "suayptalha/minGRU-LM",
		"prompt": "Once upon a time,",
		"max_tokens": 512,
		"temperature": 0.5
	}'
