// ðŸ’Ž 01_full_pipeline.sp â€” Sapphire Full End-to-End Autonomous Pipeline
// Demonstrates: Data â†’ Training â†’ Model â†’ Reasoning â†’ Memory â†’ Planning â†’ Tool use â†’ Autonomous execution

fn main_pipeline() {
    print("=====================================================================");
    print(" ðŸ’Ž SAPPHIRE COMPLETE END-TO-END AI & ML AUTONOMOUS PIPELINE");
    print("=====================================================================");
    print("");

    // 1. DATA: Load & preprocess massive dataset
    print("ðŸ“Š [1/8 DATA] Generating & Normalizing Dataset...");
    let raw_ds = ml.dataset.random(1000, 16, 2);
    let ds = raw_ds.normalize();
    let split = ds.split(0.8);
    let train_ds = split["train"];
    let val_ds   = split["val"];
    print("      Ingested {ds.size} dataset samples (80% train, 20% val).");

    // 2. TRAINING: Train multi-layer perceptron neural network
    print("\nðŸ§  [2/8 TRAINING] Building & Training Deep Neural Network...");
    let model = ml.model.mlp([16, 64, 32, 2], "relu");
    let optimizer = ml.optim.adam(0.01);

    let train_result = ml.train.fit(
        model,
        train_ds,
        ml.loss.mse,
        optimizer,
        3,
        32,
        2,
        val_ds,
        true
    );

    // 3. MODEL: Evaluate model metrics
    print("\nðŸ“ˆ [3/8 MODEL] Evaluating Model Performance Metrics...");
    let metrics = ml.train.evaluate(model, val_ds);
    print("      Validation Accuracy: {metrics.accuracy * 100}%");
    print("      Validation Loss:     {metrics.loss}");

    // 4. REASONING: Query Ollama / Groq LLM reasoning engine
    print("\nðŸ¤– [4/8 REASONING] LLM Reasoning & Intent Analysis...");
    let prompt_text = "Model validation accuracy is {metrics.accuracy * 100}%. Is this suitable for production deployment?";
    let ai_assessment = ai.prompt(prompt_text);
    print("      LLM Assessment: {ai_assessment}");

    // 5. MEMORY: Store evaluation & metrics into Vector & Short-Term Memory
    print("\nðŸ’¾ [5/8 MEMORY] Storing State in Short & Long-Term Memory...");
    agent.memory.remember("model_v1_accuracy", metrics.accuracy, {"model_type": "mlp", "epochs": 3});
    agent.memory.remember("model_v1_assessment", ai_assessment);
    agent.memory.push_chat("assistant", ai_assessment);

    let recalled = agent.memory.recall("accuracy", 1);
    let first_item = recalled[0];
    print("      Recalled Knowledge from Memory: {first_item.value}");

    // 6. PLANNING: Decompose autonomous operational goal
    print("\nðŸ—ºï¸ [6/8 PLANNING] Generating Autonomous Execution Plan...");
    let goal = "Deploy model v1, register system tool, and alert administrator.";
    let plan = agent.planning.create_plan(goal);
    print(plan.summary());

    // 7. TOOL USE: Register and execute system action tool
    print("\nðŸ”¨ [7/8 TOOL USE] Registering & Invoking Sapphire System Tool...");
    fn deploy_tool() {
        let stats = os.system_info();
        os.notify("Sapphire Pipeline", "Model v1 successfully deployed!");
        return "Tool Executed: System RAM at " + stats.ram_percent + "%";
    }
    agent.tools.register("deploy_model", "Deploys model and sends alert", deploy_tool);
    let tool_output = agent.tools.execute("deploy_model");
    print("      Tool Execution Output: {tool_output}");

    // 8. AUTONOMOUS EXECUTION: Run continuous autonomous agent loop
    print("\nðŸš€ [8/8 AUTONOMOUS EXECUTION] Launching Autonomous Loop...");
    let agent_report = agent.autonomy.run_loop(goal, 4);
    print("      Agent Status: {agent_report['finished']}");

    print("\n=====================================================================");
    print(" ðŸŽ‰ SAPPHIRE END-TO-END PIPELINE COMPLETED SUCCESSFULLY!");
    print("=====================================================================");
}

main_pipeline();

