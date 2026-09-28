
#********************************************************************************************
# calculate cost
#********************************************************************************************            
def calculate_cost( token_count_in, token_count_out, model) -> float:
    match model:
        case "claude-haiku-4-5-20251001":
            usd_per_m_input, usd_per_m_output = 1.00, 5.00
        case "claude-sonnet-5":
            usd_per_m_input, usd_per_m_output = 2.00, 10.00
        case "claude-opus-5":
            usd_per_m_input, usd_per_m_output = 5.00, 25.00
        case "gpt-4o-mini":
            usd_per_m_input, usd_per_m_output = 0.15, 0.60
        case "gpt-4o":
            usd_per_m_input, usd_per_m_output = 2.50, 10.00
        case _:  # Default / WHEN OTHERS
            raise ValueError(f"Unknown or unsupported model: {model}")    

    cost = (token_count_in * usd_per_m_input + token_count_out * usd_per_m_output) / 1_000_000
    return cost