# Test Case: High Cyclomatic Complexity
# Expected Quality: C-
# Expected Bugs: 2


def process_data(data, mode, validate, transform, filter_nulls, sort_result):
    result = []
    
    if data is not None:
        if len(data) > 0:
            if mode == "strict":
                if validate:
                    for item in data:
                        if item is not None:
                            if isinstance(item, dict):
                                if "value" in item:
                                    if item["value"] > 0:
                                        if transform:
                                            item["value"] = item["value"] * 2
                                        if filter_nulls:
                                            if item.get("status") is not None:
                                                result.append(item)
                                        else:
                                            result.append(item)
            elif mode == "relaxed":
                for item in data:
                    if item:
                        result.append(item)
        
        if sort_result:
            result.sort(key=lambda x: x.get("value", 0))
    
    return result
