use comfy_builder_core::prelude::*;
use std::error::Error;

#[derive(NodeInput)]
pub struct Input {
    left: usize,
    right: usize,
}

#[derive(NodeOutput)]
pub struct Output {
    sum: usize,
}

#[node(
    category = "Node Builder / Math",
    description = "Sums the left input with the right input"
)]
pub struct Sum;

impl<'a> Node<'a> for Sum {
    type In = Input;
    type Out = Output;
    type Error = Box<dyn Error + Send + Sync>;

    fn execute(&self, input: Self::In) -> Result<Self::Out, Self::Error> {
        Ok(Output {
            sum: input.left + input.right,
        })
    }
}

boostrap!(
    api_version: "latest"
);
