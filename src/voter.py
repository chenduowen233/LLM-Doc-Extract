# import json
# import json
# from collections import Counter
# from typing import Dict, List, Any

# class Voter:
#     def __init__(self, vote_config: Dict[str, Any]):
#         self.vote_type = vote_config.get('vote_type', 'majority')
#         self.key_parameter = vote_config.get('key_parameter')
#         self.model_weights = vote_config.get('model_weights', {})

#     def _extract_value(self, response: str) -> Any:
#         """Extracts the value of the key_parameter from a JSON string response."""
#         try:
#             data = json.loads(response)
#             if not self.key_parameter:
#                 return data  # If no key_parameter, return the whole parsed JSON object
            
#             # If key_parameter is a list, treat it as a nested key
#             if isinstance(self.key_parameter, list):
#                 current_data = data
#                 for key in self.key_parameter:
#                     if isinstance(current_data, dict) and key in current_data:
#                         current_data = current_data[key]
#                     else:
#                         return None # Key not found in nested structure
#                 return current_data
#             else:
#                 # If key_parameter is a single string, try to get it directly
#                 return data.get(self.key_parameter)
#         except json.JSONDecodeError:
#             print(f"Warning: Could not decode JSON response: {response}")
#             return None

#     def majority_vote(self, responses: Dict[str, str]) -> Dict[str, Any]:
#         """Applies majority voting to the responses."""
#         parsed_responses_data = [] # This will hold the full parsed JSON objects
#         first_full_response_data = None

#         for model_name, res_str in responses.items():
#             try:
#                 full_data = json.loads(res_str)
#                 parsed_responses_data.append(full_data)
#                 if first_full_response_data is None:
#                     first_full_response_data = full_data.copy() # Store a copy of the first full response
#             except json.JSONDecodeError:
#                 print(f"Warning: Could not decode JSON response from {model_name}: {res_str}")
#                 continue # Skip this response

#         if not parsed_responses_data:
#             return {}

#         if not self.key_parameter:
#             # If no key_parameter, vote on the entire parsed JSON object
#             # Convert dicts to string for Counter to work
#             counts = Counter(json.dumps(d, sort_keys=True) for d in parsed_responses_data)
#             most_common_str = counts.most_common(1)
#             if most_common_str:
#                 return json.loads(most_common_str[0][0])
#             return {}
#         else:
#             # If key_parameter is specified, extract the value for voting from each parsed response
#             key_values_for_voting = []
#             for data in parsed_responses_data:
#                 current_val = data
#                 if isinstance(self.key_parameter, list):
#                     for key in self.key_parameter:
#                         if isinstance(current_val, dict) and key in current_val:
#                             current_val = current_val[key]
#                         else:
#                             current_val = None
#                             break
#                 else: # single string key_parameter
#                     if isinstance(current_val, dict) and self.key_parameter in current_val:
#                         current_val = current_val[self.key_parameter]
#                     else:
#                         current_val = None
                
#                 if current_val is not None:
#                     key_values_for_voting.append(current_val)
            
#             if not key_values_for_voting:
#                 return {}

#             counts = Counter(key_values_for_voting)
#             most_common_key_value = counts.most_common(1)[0][0]

#             # Construct the final result by taking the most common key_parameter value
#             # and merging with other fields from the first valid response.
#             result = {} # Initialize result to an empty dict
#             if first_full_response_data: # Only proceed if there was at least one valid full response
#                 result = first_full_response_data.copy()
                
#                 # Update the key_parameter path with the most common value
#                 if isinstance(self.key_parameter, list):
#                     temp_data = result
#                     for i, k in enumerate(self.key_parameter):
#                         if i == len(self.key_parameter) - 1:
#                             if isinstance(temp_data, dict):
#                                 temp_data[k] = most_common_key_value
#                         else:
#                             if isinstance(temp_data, dict) and k in temp_data:
#                                 temp_data = temp_data[k]
#                             else:
#                                 # Path not found in first_full_response_data, cannot update
#                                 break
#                 else: # single string key_parameter
#                     if isinstance(result, dict) and self.key_parameter in result:
#                         result[self.key_parameter] = most_common_key_value
            
#             return result

#     def weighted_vote(self, responses: Dict[str, str]) -> Dict[str, Any]:
#         """Applies weighted voting to the responses."""
#         if not self.model_weights:
#             print("Warning: No model weights provided for weighted voting. Falling back to majority vote.")
#             return self.majority_vote(responses)

#         scores = Counter()
#         first_response_data = None

#         for model, response_str in responses.items():
#             extracted_value = self._extract_value(response_str)
#             if extracted_value is not None:
#                 if first_response_data is None:
#                     try:
#                         first_response_data = json.loads(response_str)
#                     except json.JSONDecodeError:
#                         pass

#                 weight = self.model_weights.get(model, 1.0) # Default weight is 1.0
                
#                 if not self.key_parameter:
#                     # If no key_parameter, vote on the entire extracted JSON object
#                     scores[json.dumps(extracted_value, sort_keys=True)] += weight
#                 else:
#                     # If key_parameter is specified, vote on the specific key
#                     key_val = None
#                     if isinstance(self.key_parameter, list):
#                         current_val = extracted_value
#                         for k in self.key_parameter:
#                             if isinstance(current_val, dict) and k in current_val:
#                                 current_val = current_val[k]
#                             else:
#                                 current_val = None
#                                 break
#                         key_val = current_val
#                     else:
#                         if isinstance(extracted_value, dict) and self.key_parameter in extracted_value:
#                             key_val = extracted_value[self.key_parameter]
                    
#                     if key_val is not None:
#                         scores[key_val] += weight
        
#         if not scores:
#             return {}

#         best_key_value = max(scores, key=scores.get)

#         result = {}
#         if first_response_data:
#             result = first_response_data.copy()
#             if not self.key_parameter:
#                 return json.loads(best_key_value)
#             else:
#                 # Update the key_parameter path with the best_key_value
#                 if isinstance(self.key_parameter, list):
#                     temp_data = result
#                     for i, k in enumerate(self.key_parameter):
#                         if i == len(self.key_parameter) - 1:
#                             if isinstance(temp_data, dict):
#                                 temp_data[k] = best_key_value
#                         else:
#                             if isinstance(temp_data, dict) and k in temp_data:
#                                 temp_data = temp_data[k]
#                             else:
#                                 break
#                 else:
#                     if isinstance(result, dict) and self.key_parameter in result:
#                         result[self.key_parameter] = best_key_value
        
#         return result

#     def consensus_vote(self, responses: Dict[str, str], threshold: float = 1.0) -> Dict[str, Any]:
#         """Applies consensus voting to the responses. Threshold is the proportion of models that must agree."""
#         extracted_data_list = []
#         first_response_data = None

#         for model_name, res in responses.items():
#             extracted_value = self._extract_value(res)
#             if extracted_value is not None:
#                 extracted_data_list.append(extracted_value)
#                 if first_response_data is None:
#                     try:
#                         first_response_data = json.loads(res)
#                     except json.JSONDecodeError:
#                         pass

#         if not extracted_data_list:
#             return {}

#         num_models = len(responses)

#         if not self.key_parameter:
#             # If no key_parameter, vote on the entire extracted JSON object
#             counts = Counter(json.dumps(d, sort_keys=True) for d in extracted_data_list)
#             for value_str, count in counts.items():
#                 if count / num_models >= threshold:
#                     return json.loads(value_str)
#             return {}
#         else:
#             # If key_parameter is specified, vote on the specific key
#             key_values = []
#             for data in extracted_data_list:
#                 if isinstance(self.key_parameter, list):
#                     current_val = data
#                     for k in self.key_parameter:
#                         if isinstance(current_val, dict) and k in current_val:
#                             current_val = current_val[k]
#                         else:
#                             current_val = None
#                             break
#                     if current_val is not None:
#                         key_values.append(current_val)
#                 else:
#                     if isinstance(data, dict) and self.key_parameter in data:
#                         key_values.append(data[self.key_parameter])

#             if not key_values:
#                 return {}

#             counts = Counter(key_values)
#             for key_val, count in counts.items():
#                 if count / num_models >= threshold:
#                     # Construct the final result by taking the consensus key_parameter value
#                     # and merging with other fields from the first valid response.
#                     result = {}
#                     if first_response_data:
#                         result = first_response_data.copy()
#                         if isinstance(self.key_parameter, list):
#                             temp_data = result
#                             for i, k in enumerate(self.key_parameter):
#                                 if i == len(self.key_parameter) - 1:
#                                     if isinstance(temp_data, dict):
#                                         temp_data[k] = key_val
#                                 else:
#                                     if isinstance(temp_data, dict) and k in temp_data:
#                                         temp_data = temp_data[k]
#                                     else:
#                                         break
#                         else:
#                             if isinstance(result, dict) and self.key_parameter in result:
#                                 result[self.key_parameter] = key_val
#                     return result
#             return {}

#     def vote(self, responses: Dict[str, str]) -> Dict[str, Any]:
#         """Executes the specified voting strategy."""
#         if not responses:
#             return {}

#         if self.vote_type == 'majority':
#             return self.majority_vote(responses)
#         elif self.vote_type == 'weighted':
#             return self.weighted_vote(responses)
#         elif self.vote_type == 'consensus':
#             # You might want to make the threshold configurable
#             return self.consensus_vote(responses, threshold=0.8) 
#         else:
#             print(f"Warning: Unknown vote type '{self.vote_type}'. Falling back to majority vote.")
#             return self.majority_vote(responses)

# if __name__ == '__main__':
#         # Example 1: Majority Vote (nested key)
#         voter_nested_key = Voter(vote_config={'vote_type': 'majority', 'key_parameter': ['extracted_data', 'name']})
#         responses_nested_key = {
#             "model_A": '{"extracted_data": {"name": "Alice", "age": 30, "city": "NY"}}',
#             "model_B": '{"extracted_data": {"name": "Bob", "age": 25, "city": "LA"}}',
#             "model_C": '{"extracted_data": {"name": "Alice", "age": 35, "city": "NY"}}'
#         }
#         majority_result_nested = voter_nested_key.vote(responses_nested_key)
#         print(f"Majority Vote Result (nested key): {majority_result_nested}")

#         # Example 2: Majority Vote (no key_parameter - vote on entire JSON)
#         voter_no_key = Voter(vote_config={'vote_type': 'majority', 'key_parameter': None})
#         responses_no_key = {
#             "model_A": '{"extracted_data": {"name": "Alice", "age": 30, "city": "NY"}}',
#             "model_B": '{"extracted_data": {"name": "Bob", "age": 25, "city": "LA"}}',
#             "model_C": '{"extracted_data": {"name": "Alice", "age": 30, "city": "NY"}}'
#         }
#         majority_result_no_key = voter_no_key.vote(responses_no_key)
#         print(f"Majority Vote Result (no key_parameter): {majority_result_no_key}")

#         # Example 3: Weighted Vote (nested key)
#         voter_weighted_nested = Voter(vote_config={'vote_type': 'weighted', 'key_parameter': ['extracted_data', 'name'],
#                                       'model_weights': {'model_A': 0.6, 'model_B': 0.2, 'model_C': 0.2}})
#         weighted_result_nested = voter_weighted_nested.vote(responses_nested_key)
#         print(f"Weighted Vote Result (nested key): {weighted_result_nested}")

#         # Example 4: Consensus Vote (nested key)
#         voter_consensus_nested = Voter(vote_config={'vote_type': 'consensus', 'key_parameter': ['extracted_data', 'name']})
#         consensus_result_nested = voter_consensus_nested.vote(responses_nested_key)
#         print(f"Consensus Vote Result (nested key): {consensus_result_nested}")

#         # Example 5: Consensus Vote (no consensus)
#         responses_no_consensus = {
#             "model_A": '{"extracted_data": {"name": "Alice", "age": 30, "city": "NY"}}',
#             "model_B": '{"extracted_data": {"name": "Bob", "age": 25, "city": "LA"}}',
#             "model_C": '{"extracted_data": {"name": "Charlie", "age": 35, "city": "SF"}}'
#         }
#         consensus_result_no_consensus = voter_consensus_nested.vote(responses_no_consensus)
#         print(f"Consensus Vote Result (no consensus): {consensus_result_no_consensus}")
from collections import Counter, OrderedDict
from copy import deepcopy
import json
from typing import Dict, Any

class Voter:
    def __init__(self, vote_config: Dict[str, Any]):
        self.vote_type = vote_config.get('vote_type', 'majority')
        self.key_parameter = vote_config.get('key_parameter')
        self.model_weights = vote_config.get('model_weights', {})

    def majority_vote(self, responses: Dict[str, str]) -> Dict[str, Any]:
        parsed_responses = {model: json.loads(res) for model, res in responses.items() if res}
        if not parsed_responses:
            return {}

        # 统计顶级键出现频率，保留多数模型中出现的键
        all_top_keys = []
        for data in parsed_responses.values():
            all_top_keys.extend(data.keys())
        top_key_counts = Counter(all_top_keys)
        majority_top_keys = {
            key for key, count in top_key_counts.items()
            if count >= len(parsed_responses) // 2 + 1
        }

        result = OrderedDict()

        for top_key in majority_top_keys:
            # 使用第一个包含该 top_key 的模型作为字段顺序模板
            base_data = None
            for data in parsed_responses.values():
                if top_key in data:
                    base_data = deepcopy(data[top_key])
                    break
            if not isinstance(base_data, dict):
                continue

            sub_result = OrderedDict()
            for field in base_data.keys():
                # 判断是否是需要投票的字段
                if self.key_parameter is None or field in self.key_parameter:
                    values = []
                    for data in parsed_responses.values():
                        if top_key in data and field in data[top_key]:
                            values.append(data[top_key][field])
                    if not values:
                        continue
                    field_counts = Counter(values)
                    most_common = field_counts.most_common(1)[0]
                    if most_common[1] > 1:
                        sub_result[field] = most_common[0]
                    else:
                        # 无多数值，取第一个模型中该字段值
                        sub_result[field] = base_data[field]
                else:
                    # 非投票字段，直接使用第一个模型的字段值
                    sub_result[field] = base_data[field]

            result[top_key] = sub_result

        return result
    def weighted_vote(self, responses: Dict[str, str]) -> Dict[str, Any]:
        parsed_responses = {model: json.loads(res) for model, res in responses.items() if res}
        if not parsed_responses:
            return {}

        # 顶层键多数统计
        all_top_keys = []
        for data in parsed_responses.values():
            all_top_keys.extend(data.keys())
        top_key_counts = Counter(all_top_keys)
        majority_top_keys = {
            key for key, count in top_key_counts.items()
            if count >= len(parsed_responses) // 2 + 1
        }

        result = OrderedDict()

        for top_key in majority_top_keys:
            base_data = None
            for data in parsed_responses.values():
                if top_key in data:
                    base_data = deepcopy(data[top_key])
                    break
            if not isinstance(base_data, dict):
                continue

            sub_result = OrderedDict()
            for field in base_data.keys():
                if self.key_parameter is None or field in self.key_parameter:
                    scores = Counter()
                    for model, data in parsed_responses.items():
                        if top_key in data and field in data[top_key]:
                            value = data[top_key][field]
                            weight = self.model_weights.get(model, 1.0)
                            scores[value] += weight
                    if not scores:
                        continue
                    best_value = max(scores.items(), key=lambda x: x[1])[0]
                    sub_result[field] = best_value
                else:
                    sub_result[field] = base_data[field]

            result[top_key] = sub_result
        return result
    
    def consensus_vote(self, responses: Dict[str, str], threshold: float = 0.8) -> Dict[str, Any]:
        parsed_responses = {model: json.loads(res) for model, res in responses.items() if res}
        if not parsed_responses:
            return {}

        all_top_keys = []
        for data in parsed_responses.values():
            all_top_keys.extend(data.keys())
        top_key_counts = Counter(all_top_keys)
        majority_top_keys = {
            key for key, count in top_key_counts.items()
            if count >= len(parsed_responses) // 2 + 1
        }

        result = OrderedDict()
        num_models = len(parsed_responses)

        for top_key in majority_top_keys:
            base_data = None
            for data in parsed_responses.values():
                if top_key in data:
                    base_data = deepcopy(data[top_key])
                    break
            if not isinstance(base_data, dict):
                continue

            sub_result = OrderedDict()
            for field in base_data.keys():
                if self.key_parameter is None or field in self.key_parameter:
                    values = []
                    for data in parsed_responses.values():
                        if top_key in data and field in data[top_key]:
                            values.append(data[top_key][field])
                    if not values:
                        continue
                    counts = Counter(values)
                    consensus_value = None
                    for val, cnt in counts.items():
                        if cnt / num_models >= threshold:
                            consensus_value = val
                            break
                    if consensus_value is None:
                        consensus_value = counts.most_common(1)[0][0]
                    sub_result[field] = consensus_value
                else:
                    sub_result[field] = base_data[field]

            result[top_key] = sub_result

        return result
    

    def vote(self, responses: Dict[str, str]) -> Dict[str, Any]:
        if not responses:
            return {}

        if self.vote_type == 'majority':
            return self.majority_vote(responses)
        elif self.vote_type == 'weighted':
            return self.weighted_vote(responses)
        elif self.vote_type == 'consensus':
            # You might want to make the threshold configurable
            return self.consensus_vote(responses, threshold=0.8) 
        else:
            print(f"Warning: Unknown vote type '{self.vote_type}'. Falling back to majority vote.")
            return self.majority_vote(responses)



if __name__ == '__main__':
    # 示例JSON数据（与你提供的相同）
    json_data1 = {
        "anim": {
            "description": "Whether to preserve animation frames from input files. Default is true. Setting it to false reduces animations to still images.",
            "prefix": "anim=",
            "separator": ",",
            "type": "boolean",
            "default": "true",
            "constraints": "仅允许取 'true' 或 'false'（全部小写）。"
        },
        "background": {
            "description": "Background color to add underneath the image. Applies to images with transparency and images resized with fit=pad. Accepts any CSS color using CSS4 modern syntax.",
            "prefix": "background=",
            "separator": ",",
            "type": "string",
            "default": "null",
            "constraints": "Accepts CSS colors like '#RRGGBB', 'red', or 'rgb(240,40,145)'. URL encoding may be required for certain formats (e.g., %23RRGGBB)."
        }
    }

    json_data2 = {
        "anim": {
            "description": "是否保留输入文件中的动画帧。默认为 true，设置为 false 则将动画转换为静态图像。",
            "prefix": "anim=",
            "separator": "null",
            "type": "boolean",
            "default": "true",
            "constraints": "仅允许取 'true' 或 'false'（全部小写）。"
        },
        "background": {
            "description": "添加在图像下方的背景颜色。适用于具有透明度的图像（例如 PNG）和使用 fit=pad 调整大小的图像。接受任何使用 CSS4 现代语法的 CSS 颜色。",
            "prefix": "background=",
            "separator": "null",
            "type": "string",
            "default": "null",
            "constraints": "CSS 颜色格式，如 %23RRGGBB、red、rgb%28240%2C40%2C145%29 等。必须进行 URL 编码。"
        }
    }

    json_data3 = {
        "anim": {
            "description": "是否保留动画帧，默认true，设为false转为静态图",
            "prefix": "anim=",
            "separator": "null",
            "type": "boolean",
            "default": "true",
            "constraints": "仅允许true或false"
        },
        "background": {
            "description": "图像背景色，适用于透明图和fit=pad调整的图像",
            "prefix": "background=",
            "separator": "null",
            "type": "string",
            "default": "null",
            "constraints": "支持CSS颜色格式"
        }
    }

    responses = {
        "model1": json.dumps(json_data1),
        "model2": json.dumps(json_data2),
        "model3": json.dumps(json_data3)
    }

    # 场景1: 对 prefix, type, default 字段进行投票
    vote_config1 = {
        "vote_type": "majority",
        "key_parameter": ["prefix", "separator", "type", "default"]
    }
    voter1 = Voter(vote_config1)
    result1 = voter1.vote(responses)
    print("场景1: 对 prefix, type, default 字段投票的结果:")
    print(json.dumps(result1, indent=2, ensure_ascii=False))

    # 场景2: 对所有字段投票
    vote_config2 = {
        "vote_type": "majority",
        "key_parameter": None
    }
    voter2 = Voter(vote_config2)
    result2 = voter2.vote(responses)
    print("\n场景2: 对所有字段投票的结果:")
    print(json.dumps(result2, indent=2, ensure_ascii=False))
