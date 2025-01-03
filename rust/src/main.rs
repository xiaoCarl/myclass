use std::io;

fn solve_24(nums: &[f64]) -> Vec<String> {
    let mut solutions = Vec::new();
    let ops = ['+', '-', '*', '/'];
    
    // 遍历所有可能的运算符组合
    for &a in &ops {
        for &b in &ops {
            for &c in &ops {
                // 尝试不同的括号组合
                let expressions = [
                    format!("(({} {} {}) {} {}) {} {}", nums[0], a, nums[1], b, nums[2], c, nums[3]),
                    format!("({} {} ({} {} {})) {} {}", nums[0], a, nums[1], b, nums[2], c, nums[3]),
                    format!("{} {} ({} {} ({} {} {}))", nums[0], a, nums[1], b, nums[2], c, nums[3]),
                    format!("{} {} (({} {} {}) {} {})", nums[0], a, nums[1], b, nums[2], c, nums[3]),
                    format!("({} {} {}) {} ({} {} {})", nums[0], a, nums[1], b, nums[2], c, nums[3]),
                ];
                
                for expr in expressions {
                    if let Ok(result) = eval(&expr) {
                        if (result - 24.0).abs() < 1e-6 {
                            solutions.push(expr);
                        }
                    }
                }
            }
        }
    }
    
    solutions
}

fn eval(expr: &str) -> Result<f64, String> {
    let result = meval::eval_str(expr).map_err(|e| e.to_string())?;
    Ok(result)
}

fn main() {
    println!("请输入4个数字（用空格分隔）：");
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("读取输入失败");
    
    let nums: Vec<f64> = input
        .split_whitespace()
        .map(|s| s.parse().expect("请输入有效的数字"))
        .collect();
        
    if nums.len() != 4 {
        println!("请输入恰好4个数字");
        return;
    }
    
    let solutions = solve_24(&nums);
    
    if solutions.is_empty() {
        println!("无法用这些数字得到24");
    } else {
        println!("可能的解法：");
        for sol in solutions {
            println!("{} = 24", sol);
        }
    }
}
